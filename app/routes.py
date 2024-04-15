from datetime import datetime

import flask
import flask_login
from flask import render_template, redirect
from flask_login import current_user

from app import app, store
from app.flaskuser import FlaskUser
from app.user import userservice


@app.route("/", methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect("/login", 302)


@app.route("/scrapers", methods=['GET'])
@flask_login.login_required
def scrapers():
    return render_template("scrapers.html")


@app.route("/settings", methods=['GET'])
@flask_login.login_required
def settings():
    return render_template("settings.html")


@app.route("/product/<product_id>", methods=['GET'])
@flask_login.login_required
def product(product_id):
    result = store.find(product_id)
    if len(result) > 10:
        aggregated = _aggregate(result)
        if len(aggregated) > 5:
            result = aggregated

    currencies = [obj.currency for obj in result]
    currency = currencies[0] if currencies else "pending"
    dates = [obj.date for obj in result]
    prices = [float(obj.price) for obj in result]
    name = result[0].name
    if not name:
        name = "pending"
    return render_template("product.html", prices=prices, dates=dates, name=name, currency=currency)


@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def do_login():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    user = FlaskUser(username, password)
    is_authenticated = userservice.is_authenticated(user)
    if not is_authenticated:
        return flask.redirect(flask.url_for("login"))

    flask_login.login_user(FlaskUser(username, password))
    return flask.redirect("/")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return render_template('index.html')


def _aggregate(products: list) -> list:
    day_dict = {}

    for product in products:
        date_obj = datetime.strptime(product.date, '%d.%m.%Y - %H:%M:%S')
        date_key = date_obj.date()

        if date_key not in day_dict:
            day_dict[date_key] = product
        else:
            day_dict[date_key] = product

    entries = list(day_dict.values())
    for entry in entries:
        entry.date = entry.date.split(' - ')[0]

    return entries

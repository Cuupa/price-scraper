from datetime import datetime

from flask import render_template

from app import app, store


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/scrapers", methods=['GET'])
def scrapers():
    return render_template("scrapers.html")


@app.route("/settings", methods=['GET'])
def settings():
    return render_template("settings.html")


@app.route("/product/<product_id>", methods=['GET'])
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
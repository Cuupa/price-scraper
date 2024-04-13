import flask_login
from flask import request

from app import app, scheduler


@app.route("/api/settings", methods=['GET'])
@flask_login.login_required
def api_settings():
    return {'interval': scheduler.interval}


@app.route("/api/settings/interval", methods=['POST'])
@flask_login.login_required
def api_interval():
    data = request.get_json()
    scheduler.update_settings(int(data['interval']))

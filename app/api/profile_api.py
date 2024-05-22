import flask_login
from flask import request

from app import app


@app.route("/api/profile/password", methods=['POST'])
@flask_login.login_required
def update_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']
    confirm_password = data['confirmPassword']
    pass

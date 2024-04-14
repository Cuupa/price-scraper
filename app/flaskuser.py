import flask_login


class FlaskUser(flask_login.UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password


import flask_login


class FlaskUser(flask_login.UserMixin):
    def __init__(self, email, password):
        self.id = email
        self.password = password

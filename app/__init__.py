from flask_login import LoginManager
from flask import Flask
from flask_sock import Sock

from app.user import userservice

app = Flask(__name__)
sock = Sock(app)
from app import routes
from app import api
from app.scraping import scheduler

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    return userservice.get(username)


scheduler.run()

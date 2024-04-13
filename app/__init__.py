from flask_login import LoginManager
from flask import Flask
from flask_sock import Sock

from app.product_persistence.store import Store
from app.scraping.scrapermanager import ScraperManager
from app.user import userservice

app = Flask(__name__)
sock = Sock(app)

store = Store()

scraper_manager = ScraperManager()
from app.scraping.scheduler import Scheduler

scheduler = Scheduler(scraper_manager)
scheduler.run()

from app import routes
from app import api
from app.scraping import scheduler

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    return userservice.get(username)


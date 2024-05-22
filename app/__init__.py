from flask import Flask
from flask_sock import Sock

from app.product_persistence.store import Store
from app.scraping.scrapermanager import ScraperManager

app = Flask(__name__)
sock = Sock(app)

store = Store()

scraper_manager = ScraperManager()
from app.scraping.scheduler import Scheduler

scheduler = Scheduler(scraper_manager)
scheduler.run()

from app import routes
from app import api
from app import websocket_server

from app import app
from app.scraping import scraper
from flask import request


@app.route("/api/scraper/register", methods=['POST'])
def api_register():
    data = request.get_json()
    url = data['url']
    name = data['name']
    scraper.register(name, url)
    return '', 200


@app.route("/api/scrapers", methods=['GET'])
def api_scrapers():
    return {'scrapers': scraper.scrapers}

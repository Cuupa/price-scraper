from app import app, scraper_manager
from flask import request


@app.route("/api/scraper/register", methods=['POST'])
def api_register():
    data = request.get_json()
    url = data['url']
    name = data['name']
    scraper_manager.register(name, url)
    return '', 200


@app.route("/api/scrapers", methods=['GET'])
def api_scrapers():
    return {'scrapers': scraper_manager.scrapers}

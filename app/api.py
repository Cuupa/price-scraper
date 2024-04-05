from flask import request

from app import app, scraper, store, scheduler, notifications
from app.dataclasses.product import Product


@app.route('/api/scraper/register', methods=['POST'])
def api_register():
    data = request.get_json()
    url = data['url']
    name = data['name']
    scraper.register(name, url)
    return '', 200


@app.route('/api/notification', methods=['PUT'])
def register_notification_service():
    data = request.get_json()
    notification_type = data['type']
    if notification_type is 'ntfy':
        url = data['url']
        enabled = data['enabled']
        notifications.register(notification_type, url, enabled)
        return '', 200
    return '', 501


@app.route('/api/notification', methods=['DELETE'])
def delete_notification_service():
    data = request.get_json()


@app.route('/api/product', methods=['PUT'])
def api_add():
    data = request.get_json()

    if data['type'] == 'item':
        success = store.store_product(data['url'])
        if success:
            scheduler.scrape_products()
            return data['url'] + ' successfully added'
        else:
            return data['url'] + ' already exists'


@app.route('/api/products', methods=['GET'])
def api_products():
    return {'products': [(sanitize(entry)) for entry in store.all_products()]}


@app.route('/api/product/<product_id>', methods=['DELETE'])
def delete_prodcut(product_id):
    store.remove_product(product_id)
    return '', 200


@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    points = store.find(product_id)
    return {'product': points}, 200


@app.route('/api/scrapers', methods=['GET'])
def api_scrapers():
    return {'scrapers': scraper.scrapers}


@app.route('/api/settings', methods=['GET'])
def api_settings():
    return {'interval': scheduler.interval}


@app.route('/api/settings/interval', methods=['POST'])
def api_interval():
    data = request.get_json()
    scheduler.update_settings(int(data['interval']))


def sanitize(x: Product) -> Product:
    x.url = replace_none(x.url)
    x.lowest_price = replace_none(x.lowest_price)
    x.current_price = replace_none(x.current_price)
    x.currency = replace_none(x.currency)
    return x


def replace_none(string: str) -> str:
    return '-' if string is None else string

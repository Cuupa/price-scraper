from flask import request

from app import app
from app.scraping import scheduler
from app.product_persistence import store
from app.dataclasses.product import Product


@app.route("/api/product", methods=['PUT'])
def api_add():
    data = request.get_json()

    if data['type'] == 'item':
        success = store.store_product(data['url'])
        if success:
            print("Added product, attempting scrape")
            scheduler.scrape_products()
            return data['url'] + " successfully added"
        else:
            return data['url'] + " already exists"


@app.route("/api/products", methods=['GET'])
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


def sanitize(x: Product) -> Product:
    x.url = replace_none(x.url)
    x.lowest_price = replace_none(x.lowest_price)
    x.current_price = replace_none(x.current_price)
    x.currency = replace_none(x.currency)
    return x


def replace_none(string: str) -> str:
    return "-" if string is None else string

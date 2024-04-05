from datetime import datetime

from app.product_persistence import product_store as product_store, product_history as product_history
from app.dataclasses.product import Product
from app.dataclasses.product_history_point import ProductHistoryPoint


def store_product(url: str):
    return product_store.store_item(url)


def all_products() -> list:
    products = product_store.all_products()
    values = []

    for product in products:
        history = product_history.search(product[0])
        current_price = None
        lowest_price = None
        currency = None
        if len(history) > 0:
            current_price = max(history, key=lambda x: datetime.strptime(x[3], "%d.%m.%Y - %H:%M:%S"))[1]
            lowest_price = min(history, key=lambda x: x[1])[1]
            currency = history[0][2]

        obj = Product(id=product[0],
                      url=product[1],
                      name=product[2],
                      lowest_price=lowest_price,
                      current_price=current_price,
                      currency=currency)
        values.append(obj)
    return values


def _is_lower(price: str, lowest_price: str):
    price_number = float(price.replace(",", ".").replace("€", ""))
    lowest_price_number = float(lowest_price.replace(",", ".").replace("€", ""))
    return price_number < lowest_price_number


def _to_number(number: str) -> float:
    return float(number.replace(",", ".").replace("€", "").strip())


def add_point(product_id: int, name: str, price: str, currency: str, date_time):
    product_store.update(product_id, name)
    product_history.insert(product_id, price, currency, date_time)


def find(product_id):
    product = product_store.find(product_id)
    history = product_history.search(product_id)
    list = sorted(history, key=lambda x: datetime.strptime(x[3], "%d.%m.%Y - %H:%M:%S"))
    points = []
    for point in list:
        obj = ProductHistoryPoint(id=product_id, name=product[0][2], url=product[0][1], price=point[1], currency=point[2],
                                  date=point[3])
        points.append(obj)
    return points


def remove_product(product_id):
    product_store.remove(product_id)
    product_history.remove(product_id)
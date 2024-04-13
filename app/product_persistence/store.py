from datetime import datetime

from app.product_persistence import product_persistence as product_store, product_history_persistence as product_history
from app.dataclasses.product import Product
from app.dataclasses.product_history_point import ProductHistoryPoint
from app.product_persistence.product_history_persistence import ProductHistoryPersistence
from app.product_persistence.product_persistence import ProductPersistence


class Store:
    def __init__(self):
        self.product_store = ProductPersistence()
        self.product_history_store = ProductHistoryPersistence()

    def store_product(self, url: str):
        return self.product_store.store_item(url)

    def all_products(self) -> list:
        products = self.product_store.all_products()
        values = []

        for product in products:
            history = self.product_history_store.search(product[0])
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

    def _is_lower(self, price: str, lowest_price: str):
        price_number = float(price.replace(",", ".").replace("€", ""))
        lowest_price_number = float(lowest_price.replace(",", ".").replace("€", ""))
        return price_number < lowest_price_number

    def _to_number(self, number: str) -> float:
        return float(number.replace(",", ".").replace("€", "").strip())

    def add_point(self, product_id: int, name: str, price: str, currency: str, date_time):
        self.product_store.update(product_id, name)
        self.product_history_store.insert(product_id, price, currency, date_time)

    def find(self, product_id):
        product = self.product_store.find(product_id)
        history = self.product_history_store.search(product_id)
        sorted_list = sorted(history, key=lambda x: datetime.strptime(x[3], "%d.%m.%Y - %H:%M:%S"))
        points = []
        for point in sorted_list:
            obj = ProductHistoryPoint(id=product_id, name=product[0][2], url=product[0][1], price=point[1],
                                      currency=point[2],
                                      date=point[3])
            points.append(obj)
        return points

    def remove_product(self, product_id):
        self.product_store.remove(product_id)
        self.product_history_store.remove(product_id)

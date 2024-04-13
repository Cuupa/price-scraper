import requests

from app.notifications import notifications_store
from app.dataclasses.product import Product
import base64

from app.notifications.notifications_store import NotificationsPersistence


class Notifications:
    def __init__(self):
        self.notifications_store = NotificationsPersistence()

    def notify(self, product: Product, price: float):
        notification = self.notifications_store.search('ntfy')

        headers = {"Priority": str(notification.priority)}

        if notification.username is not None:
            auth_bytes = bytes(notification.username + ":" + notification.password, 'UTF-8')
            headers['Authorization'] = f'Basic {str(base64.b64encode(auth_bytes))}'
        elif notification.accesstoken is not None:
            headers['Authorization'] = f'Bearer {notification.accesstoken}'

        payload = f'Price of {product} has dropped to {price}'
        requests.post(f'{notification.url}/{notification.topic}',
                      data=payload,
                      headers=headers)

    def filter_ntfy(self, notification):
        return notification.type == "ntfy"

    def register(self, notification):
        self.notifications_store.save(notification)

    def get(self, notification_type: str):
        return self.notifications_store.search(notification_type)

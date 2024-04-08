import requests

from app.notifications import notifications_store
from app.dataclasses.product import Product
import base64


def notify(product: Product, price: float):
    notifications = notifications_store.search('ntfy')

    for notification in notifications:
        headers = {"Priority": notification.priority}

        if notification.username is not None:
            auth_bytes = bytes(notification.username + ":" + notification.password, 'UTF-8')
            headers['Authorization'] = 'Basic ' + str(base64.b64encode(auth_bytes))
        elif notification.accesstoken is not None:
            headers['Authorization'] = 'Bearer ' + notification.accesstoken

        payload = f'Price of {product} has dropped to {price}'
        requests.post(notification.url,
                      data=payload.encode(encoding='utf-8'),
                      headers=headers)


def filter_ntfy(notification):
    return notification.type == "ntfy"


def register(notification):
    notifications_store.save(notification)


def get(notification_type: str):
    return notifications_store.search(notification_type)

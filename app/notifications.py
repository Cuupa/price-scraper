import requests

from app import notifications_store


def notify(payload: str):
    notifications = notifications_store.get_all()
    ntfy = filter(filter_ntfy, notifications)
    for notification in ntfy:
        requests.post(notification.url, data=payload.encode(encoding='utf-8'))
    pass


def filter_ntfy(notification):
    return notification.type == "ntfy"


def register(notification_type: str, url: str, enabled: bool):
    notifications_store.save(notification_type, url, enabled)

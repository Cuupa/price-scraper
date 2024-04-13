from flask import request

from app import app
from app.dataclasses.ntfy import ntfy
from app.notifications.notifications import Notifications

notifications = Notifications()

@app.route('/api/notification', methods=['PUT'])
def register_notification_service():
    data = request.get_json()

    if data['type'] == 'ntfy':
        if save_ntfy_settings(data):
            return '', 200
    return '', 501


def save_ntfy_settings(data) -> bool:
    if 'url' not in data or not data['url']:
        return False
    if 'topic' not in data or not data['topic']:
        return False

    password = None
    accesstoken = None
    username = None

    if 'password' in data and len(data['password']) > 0:
        password = data['password']
        username = data['username']
    elif 'accesstoken' in data and len(data['accesstoken']) > 0:
        accesstoken = data['accesstoken']

    notification = ntfy(url=data['url'],
                        enabled=data['enabled'],
                        priority=data['priority'],
                        topic=data['topic'],
                        username=username,
                        password=password,
                        accesstoken=accesstoken)
    notifications.register(notification)
    return True


@app.route('/api/notification/<notification_type>', methods=['GET'])
def load_notifications(notification_type: str):
    notification = notifications.get(notification_type)
    if notification is None:
        return '{}', 200
    return {
        'url': notification.url,
        'topic': notification.topic,
        'enabled': notification.enabled,
        'priority': notification.priority,
        'username': notification.username,
        'password': '*********',
        'accesstoken': '*********' if notification.accesstoken else None
    }, 200

import flask_login
from flask import request

from app import app
from app.dataclasses.ntfy import ntfy
from app.notifications import notifications


@app.route('/api/notification', methods=['PUT'])
@flask_login.login_required
def register_notification_service():
    data = request.get_json()

    if data['type'] == 'ntfy':

        if 'url' not in data or not data['url']:
            return '', 501
        if 'topic' not in data or not data['topic']:
            return '', 501

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
        return '', 200
    return '', 501


@app.route('/api/notification/<notification_type>', methods=['GET'])
@flask_login.login_required
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


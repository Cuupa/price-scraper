from flask import request

from app import app, notifications


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

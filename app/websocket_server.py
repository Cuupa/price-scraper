import json
from app import sock
from simple_websocket import Server

connections = set()


def send_message(product, price):
    if connections:
        message = {'event': 'change',
                   'product': product.name,
                   'price': price}

        closed_connections = []

        for websocket in connections:
            if websocket.connected:
                websocket.send(json.dumps(message))
            else:
                closed_connections.append(websocket)

        for connection in closed_connections:
            connections.remove(connection)


@sock.route('/websocket')
def handle_websocket(websocket: Server):
    connections.add(websocket)
    while True:
        websocket.receive()

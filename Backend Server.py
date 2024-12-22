backend.py

import http.server
import socketserver
import json
from geopy.distance import geodesic
import random
import threading
import socketio

# -------------------------------
# MOCK DATABASE
# -------------------------------
buses = {
    1: {
        'bus_number': 'Bus101',
        'current_location': '12.9716,77.5946',
        'route': 'Station A -> Station B -> Station C',
        'speed': 40,  # km/h
        'has_crossed_stop': False,
        'fee': 1.5
    }
}

users = {
    1: {
        'name': 'Alice',
        'balance': 10.0
    }
}

# -------------------------------
# SOCKET.IO SERVER (Driver Communication)
# -------------------------------
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print(f"{sid} connected")


@sio.event
def send_message(sid, data):
    print(f"Message from {sid}: {data}")
    sio.emit('receive_message', data)


@sio.event
def disconnect(sid):
    print(f"{sid} disconnected")


# -------------------------------
# HTTP SERVER (API Endpoints)
# -------------------------------
class BusTrackingHandler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        path = self.path.split('/')
        
        # Get ETA
        if len(path) >= 4 and path[1] == 'bus' and path[3] == 'eta':
            bus_id = int(path[2])
            stop_location = path[4]
            if bus_id in buses:
                bus = buses[bus_id]
                distance = random.uniform(1, 10)  # Mocked distance
                speed = bus['speed']
                eta = distance / speed * 60  # minutes
                self._send_response({
                    'bus_number': bus['bus_number'],
                    'estimated_time': f"{eta:.2f} minutes",
                    'current_location': bus['current_location']
                })
            else:
                self._send_response({'error': 'Bus not found'}, 404)

        # Get Route
        elif len(path) >= 3 and path[1] == 'bus' and path[3] == 'route':
            bus_id = int(path[2])
            if bus_id in buses:
                self._send_response({
                    'bus_number': buses[bus_id]['bus_number'],
                    'route': buses[bus_id]['route']
                })
            else:
                self._send_response({'error': 'Bus not found'}, 404)

        # Get Traffic
        elif len(path) >= 3 and path[1] == 'traffic':
            location = path[2]
            traffic_level = random.choice(['Low', 'Medium', 'High'])
            self._send_response({
                'location': location,
                'traffic': traffic_level
            })

        else:
            self._send_response({'error': 'Invalid endpoint'}, 404)

    def do_POST(self):
        path = self.path.split('/')
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length).decode('utf-8'))

        # Pay Fare
        if len(path) >= 4 and path[1] == 'user' and path[3] == 'pay':
            user_id = int(path[2])
            bus_id = body.get('bus_id')
            if user_id in users and bus_id in buses:
                user = users[user_id]
                bus = buses[bus_id]
                if user['balance'] >= bus['fee']:
                    user['balance'] -= bus['fee']
                    self._send_response({
                        'message': 'Fare payment successful',
                        'remaining_balance': user['balance']
                    })
                else:
                    self._send_response({'error': 'Insufficient balance'}, 400)
            else:
                self._send_response({'error': 'User or Bus not found'}, 404)


# -------------------------------
# START SERVERS
# -------------------------------
def start_http_server():
    with socketserver.ThreadingTCPServer(('localhost', 8080), BusTrackingHandler) as httpd:
        print("HTTP server running on http://localhost:8080")
        httpd.serve_forever()


def start_socketio_server():
    import eventlet
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)


if _name_ == '_main_':
    http_thread = threading.Thread(target=start_http_server)
    socketio_thread = threading.Thread(target=start_socketio_server)

    http_thread.start()
    socketio_thread.start()

    http_thread.join()
    socketio_thread.join()

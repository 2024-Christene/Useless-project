# backend.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

DATA_FILE = 'buses.json'

class BusTrackingHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _read_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        return []

    def _write_data(self, data):
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)

    def do_GET(self):
        self._set_headers()
        data = self._read_data()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        bus = json.loads(post_data)

        data = self._read_data()
        data.append(bus)
        self._write_data(data)

        self._set_headers()
        self.wfile.write(json.dumps(bus).encode('utf-8'))

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        updated_bus = json.loads(put_data)

        data = self._read_data()
        for bus in data:
            if bus['id'] == updated_bus['id']:
                bus.update(updated_bus)

        self._write_data(data)
        self._set_headers()
        self.wfile.write(json.dumps(updated_bus).encode('utf-8'))

    def do_DELETE(self):
        content_length = int(self.headers['Content-Length'])
        delete_data = self.rfile.read(content_length)
        bus_id = json.loads(delete_data)['id']

        data = self._read_data()
        data = [bus for bus in data if bus['id'] != bus_id]
        self._write_data(data)

        self._set_headers()
        self.wfile.write(json.dumps({'message': 'Bus deleted'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=BusTrackingHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if _name_ == '_main_':
    run()
buses.json=[]

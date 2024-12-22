# frontend.py
import tkinter as tk
from tkinter import messagebox
import requests

API_URL = 'http://127.0.0.1:8080'

class BusTrackingApp:

    def _init_(self, root):
        self.root = root
        self.root.title("Bus Tracking App")

        self.bus_list = tk.Listbox(root)
        self.bus_list.pack(fill=tk.BOTH, expand=True)

        self.add_bus_frame = tk.Frame(root)
        self.add_bus_frame.pack(fill=tk.X)

        tk.Label(self.add_bus_frame, text="Bus Number:").pack(side=tk.LEFT)
        self.bus_number_entry = tk.Entry(self.add_bus_frame)
        self.bus_number_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.add_bus_frame, text="Latitude:").pack(side=tk.LEFT)
        self.latitude_entry = tk.Entry(self.add_bus_frame)
        self.latitude_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.add_bus_frame, text="Longitude:").pack(side=tk.LEFT)
        self.longitude_entry = tk.Entry(self.add_bus_frame)
        self.longitude_entry.pack(side=tk.LEFT, padx=5)

        self.add_bus_button = tk.Button(self.add_bus_frame, text="Add Bus", command=self.add_bus)
        self.add_bus_button.pack(side=tk.LEFT, padx=5)

        self.load_buses()

    def load_buses(self):
        response = requests.get(API_URL)
        if response.status_code == 200:
            buses = response.json()
            self.bus_list.delete(0, tk.END)
            for bus in buses:
                self.bus_list.insert(tk.END, f"Bus {bus['number']}: ({bus['latitude']}, {bus['longitude']})")

    def add_bus(self):
        bus_number = self.bus_number_entry.get()
        latitude = float(self.latitude_entry.get())
        longitude = float(self.longitude_entry.get())

        bus = {'id': self.get_next_id(), 'number': bus_number, 'latitude': latitude, 'longitude': longitude}
        response = requests.post(API_URL, json=bus)
        if response.status_code == 200:
            self.load_buses()
        else:
            messagebox.showerror("Error", "Failed to add bus")

    def get_next_id(self):
        response = requests.get(API_URL)
        if response.status_code == 200:
            buses = response.json()
            return max(bus['id'] for bus in buses) + 1 if buses else 1

if _name_ == "_main_":
    root = tk.Tk()
    app = BusTrackingApp(root)
    root.mainloop()

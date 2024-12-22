import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# Mock Bus Data
bus_data = {
    "current_location": {"lat": 37.7749, "lng": -122.4194},
    "route": ["Stop A", "Stop B", "Stop C", "Destination"],
    "speed": 50,  # km/h
    "traffic": "Moderate",
    "estimated_time": {"Stop A": "5 min", "Stop B": "15 min", "Destination": "30 min"},
    "current_stop": "Stop A"
}

# Payment data
payments = []

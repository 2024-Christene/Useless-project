# frontend.py
import tkinter as tk
from tkinter import messagebox
import requests
# -------------------------------
# GUI APPLICATION
# -------------------------------
class BusTrackingApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Bus Tracking System")
        self.root.geometry("400x500")

        # ETA
        tk.Label(root, text="Bus ID:").pack()
        self.bus_id_entry = tk.Entry(root)
        self.bus_id_entry.pack()

        tk.Label(root, text="Stop:").pack()
        self.stop_entry = tk.Entry(root)
        self.stop_entry.pack()

        tk.Button(root, text="Get ETA", command=self.get_eta).pack(pady=10)

        # Balance Management
        tk.Label(root, text="User ID:").pack()
        self.user_id_entry = tk.Entry(root)
        self.user_id_entry.pack()

        tk.Label(root, text="Amount:").pack()
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        tk.Button(root, text="Add Balance", command=self.add_balance).pack(pady=10)
        tk.Button(root, text="Pay Fare", command=self.pay_fare).pack(pady=10)

    def get_eta(self):
        bus_id = self.bus_id_entry.get()
        stop = self.stop_entry.get()
        try:
            response = requests.get(f"http://localhost:8080/bus/{bus_id}/eta/{stop}")
            data = response.json()
            messagebox.showinfo("ETA", f"ETA: {data['estimated_time']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch ETA: {e}")

    def add_balance(self):
        user_id = self.user_id_entry.get()
        amount = self.amount_entry.get()
        try:
            response = requests.post(f"http://localhost:8080/user/{user_id}/add_balance", json={'amount': amount})
            data = response.json()
            messagebox.showinfo("Success", f"New Balance: {data['current_balance']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add balance: {e}")

    def pay_fare(self):
        user_id = self.user_id_entry.get()
        try:
            response = requests.post(f"http://localhost:8080/user/{user_id}/pay", json={'bus_id': 1})
            data = response.json()
            messagebox.showinfo("Success", data['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pay fare: {e}")


# -------------------------------
# RUN THE GUI
# -------------------------------
if _name_ == '_main_':
    root = tk.Tk()
    app = BusTrackingApp(root)
    root.mainloop()


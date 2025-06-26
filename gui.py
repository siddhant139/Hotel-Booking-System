# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from hotel import Hotel

class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("700x500")
        style = ttk.Style(self)
        style.theme_use('clam')

        self.hotel = Hotel()
        # add rooms
        for id in range(101, 111):
            self.hotel.add_room(id, "Standard", 1000)
        for id in range(201, 211):
            self.hotel.add_room(id, "Deluxe", 1500)
        for id in range(301, 311):
            self.hotel.add_room(id, "Suite", 2000)
        # add customers
        names = ["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy"]
        for idx, name in enumerate(names, start=1):
            self.hotel.add_customer(idx, name)

        # tabs
        self.tabs = ttk.Notebook(self)
        self.tab_rooms = ttk.Frame(self.tabs)
        self.tab_occupied = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_rooms, text="Rooms")
        self.tabs.add(self.tab_occupied, text="Occupied")
        self.tabs.pack(fill="both", expand=True)

        # Rooms tab
        self.room_tree = ttk.Treeview(self.tab_rooms, columns=("ID","Type","Price","Available"), show="headings")
        for col in self.room_tree["columns"]:
            self.room_tree.heading(col, text=col)
            self.room_tree.column(col, anchor="center")
        self.room_tree.pack(fill="both", expand=True, padx=10, pady=5)
        # buttons
        btn_frame = ttk.Frame(self.tab_rooms)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Refresh", command=self.populate_rooms).grid(row=0,column=0, padx=5)
        ttk.Button(btn_frame, text="Check In", command=self.check_in).grid(row=0,column=1, padx=5)
        ttk.Button(btn_frame, text="Check Out", command=self.check_out).grid(row=0,column=2, padx=5)

        # Occupied tab
        self.occ_tree = ttk.Treeview(self.tab_occupied, columns=("Customer","RoomID"), show="headings")
        self.occ_tree.heading("Customer", text="Customer")
        self.occ_tree.heading("RoomID", text="Room ID")
        self.occ_tree.pack(fill="both", expand=True, padx=10, pady=5)
        ttk.Button(self.tab_occupied, text="Refresh", command=self.populate_occupied).pack(pady=5)

        # status bar
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w").pack(fill="x", side="bottom")
        self.set_status("Ready")

        self.populate_rooms()
        self.populate_occupied()

    def set_status(self, msg):
        self.status.set(msg)

    def populate_rooms(self):
        for i in self.room_tree.get_children():
            self.room_tree.delete(i)
        for r in self.hotel.rooms:
            self.room_tree.insert("", "end", values=(r.id, r.type, r.price, "Yes" if r.available else "No"))
        self.set_status("Room list updated")

    def populate_occupied(self):
        for i in self.occ_tree.get_children():
            self.occ_tree.delete(i)
        for c in self.hotel.customers:
            if c.room_id is not None:
                self.occ_tree.insert("", "end", values=(c.name, c.room_id))
        self.set_status("Occupied list updated")

    def check_in(self):
        win = tk.Toplevel(self)
        win.title("Select Customer")
        ttk.Label(win, text="Customer:").pack(padx=10, pady=5)
        cust_names = [f"{c.id}: {c.name}" for c in self.hotel.customers] + ["New Customer..."]
        var = tk.StringVar(value=cust_names[0])
        cb = ttk.Combobox(win, values=cust_names, textvariable=var, state="readonly")
        cb.pack(padx=10, pady=5)
        ttk.Button(win, text="OK", command=win.destroy).pack(pady=5)
        win.transient(self); win.grab_set(); self.wait_window(win)
        sel = var.get()
        if sel == "New Customer...":
            name = self.prompt("Enter new customer name")
            if name:
                new_id = max(c.id for c in self.hotel.customers) + 1
                self.hotel.add_customer(new_id, name)
                cust_id = new_id
            else:
                return
        else:
            cust_id = int(sel.split(":")[0])

        rid_str = self.prompt("Enter Room ID")
        try:
            room_id = int(rid_str)
        except:
            return
        msg = self.hotel.check_in(cust_id, room_id)
        messagebox.showinfo("Check In", msg)
        self.set_status(msg)
        self.populate_rooms()
        self.populate_occupied()

    def check_out(self):
        cid_str = self.prompt("Enter Customer ID to Check Out")
        try:
            cid = int(cid_str)
        except:
            return
        msg = self.hotel.check_out(cid)
        messagebox.showinfo("Check Out", msg)
        self.set_status(msg)
        self.populate_rooms()
        self.populate_occupied()

    def prompt(self, text):
        win = tk.Toplevel(self)
        win.title(text)
        ttk.Label(win, text=text).pack(padx=10, pady=5)
        var = tk.StringVar()
        ttk.Entry(win, textvariable=var).pack(padx=10, pady=5)
        ttk.Button(win, text="OK", command=win.destroy).pack(pady=5)
        win.transient(self); win.grab_set(); self.wait_window(win)
        return var.get()

if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()

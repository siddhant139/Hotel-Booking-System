# hotel.py
class Room:
    def __init__(self, id, rtype, price):
        self.id = id
        self.type = rtype
        self.price = price
        self.available = True

class Customer:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.room_id = None

class Hotel:
    def __init__(self):
        self.rooms = []
        self.customers = []

    def add_room(self, id, rtype, price):
        self.rooms.append(Room(id, rtype, price))

    def add_customer(self, id, name):
        self.customers.append(Customer(id, name))

    def check_in(self, cust_id, room_id):
        room = next((r for r in self.rooms if r.id == room_id), None)
        cust = next((c for c in self.customers if c.id == cust_id), None)
        if not room or not cust:
            return "Invalid ID"
        if not room.available:
            return f"Room {room_id} not available"
        room.available = False
        cust.room_id = room_id
        return f"{cust.name} checked into room {room_id}"

    def check_out(self, cust_id):
        cust = next((c for c in self.customers if c.id == cust_id), None)
        if not cust or cust.room_id is None:
            return "Nothing to check out"
        room = next(r for r in self.rooms if r.id == cust.room_id)
        room.available = True
        msg = f"{cust.name} checked out of room {cust.room_id}"
        cust.room_id = None
        return msg

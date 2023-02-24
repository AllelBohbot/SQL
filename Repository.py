import sqlite3
from DAO import Hats, Suppliers, Orders
from DTO import Order


# def check_validity(hat):
#     if hat.quantity == 0:
#         Hats.remove(hat.id)


class Repository:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.hats = Hats(self.conn)  # create DAO for hats table
        self.orders = Orders(self.conn)  # create DAO for orders table
        self.suppliers = Suppliers(self.conn)  # create DAO for suppliers table

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""CREATE TABLE hats(
                                id INT PRIMARY KEY,
                                topping TEXT NOT NULL,  
                                supplier INT REFERENCES suppliers(id), 
                                quantity INT);
                                
                                CREATE TABLE suppliers(
                                id INT PRIMARY KEY, 
                                name TEXT NOT NULL);
                                
                                CREATE TABLE orders(id INT PRIMARY KEY, 
                                location TEXT NOT NULL, 
                                hat INT REFERENCES hats(id));""")


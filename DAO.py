import DTO


class Hats:

    def __init__(self, conn):
        self._conn = conn
        self.c = self._conn.cursor()

    def insert(self, hat):
        self._conn.execute("""
                      INSERT INTO hats(id, topping, supplier, quantity) VALUES (?, ?, ?, ?)
                  """, [hat.id, hat.topping, hat.supplier, hat.quantity])

    def find(self, hat_topping):
        self.c.execute(
            """SELECT id, quantity, supplier FROM hats WHERE topping = ? ORDER BY supplier ASC""", (hat_topping, ))
        output = self.c.fetchone()
        return output[0], output[1], output[2]

    def decrease_quantity(self, hat_id):
        self.c.execute(""" SELECT quantity FROM hats WHERE id=? """, (hat_id, ))
        update = int(*self.c.fetchone()) - 1
        self.c.execute(""" UPDATE hats SET quantity=? WHERE id=? """, (update, hat_id))

    def remove(self, hat_id):
        self.c.execute(""" DELETE FROM hats WHERE id=?""", (hat_id, ))


class Suppliers:
    def __init__(self, conn):
        self._conn = conn
        self.c = self._conn.cursor()

    def insert(self, supplier):
        self._conn.execute(""" INSERT INTO suppliers(id, name) VALUES(?,?)""", [supplier.id, supplier.name])

    def findSupplierName(self, supplier_id):
        self.c.execute(""" SELECT name FROM suppliers WHERE id = ? """, (supplier_id, ))
        output = self.c.fetchone()
        return output[0]


class Orders:
    def __init__(self, conn):
        self._conn = conn
        self.c = self._conn.cursor()

    def insert(self, order):
        self._conn.execute(
            """ INSERT INTO orders(id, location, hat) VALUES(?, ?, ?)""", (order.id, order.location,
                                                                                    order.hat))

    def get_max_id(self):
        self.c.execute(""" SELECT MAX(id) FROM orders""")
        temp_id = self.c.fetchone()[0]
        if temp_id is None:
            return 0
        else:
            return temp_id

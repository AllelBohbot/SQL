import sys

from DAO import Hats, Suppliers
from DTO import Order, Supplier, Hat
import atexit
from Repository import Repository


def parse_config_file(path, repo):
    with open(path, "r") as config_file:
        config_file = config_file.readlines()
        sizes = config_file[0].split(",");
        hats_size = int(sizes[0])
        # Parse and add input hats to table
        for i in range(1, hats_size + 1):
            if i != hats_size:
                current_line = config_file[i][0:len(config_file[i]) - 1].split(",")
            else:
                current_line = config_file[i].split(",")
            hatid = int(current_line[0])
            topping = current_line[1]
            supplier = int(current_line[2])
            quantity = int(current_line[3])
            hat = Hat(hatid, topping, supplier, quantity)
            repo.hats.insert(hat)

        # Parse and add input suppliers to table
        for i in range(hats_size + 1, len(config_file)):
            if i != len(config_file)-1:
                current_line = config_file[i][0:len(config_file[i]) - 1].split(",")
            else:
                current_line = config_file[i].split(",")
            supplier_id = int(current_line[0])
            name = current_line[1]
            supplier = Supplier(supplier_id, name)
            repo.suppliers.insert(supplier)


def main():
    config_file = sys.argv[1]
    orders_file = sys.argv[2]
    output_file = sys.argv[3]

    repo = Repository(sys.argv[4])
    atexit.register(repo.close)
    repo.create_tables()
    parse_config_file(config_file, repo)
    with open(orders_file, "r") as orders, open(output_file, "w") as output:
        orders = orders.readlines()

        for order in orders:
            order=order.replace("\n", "")
            order_info = order.split(",")
            order_location = order_info[0]
            order_topping = order_info[1]
            hat_id, hat_quantity, supplier = repo.hats.find(order_topping)
            order_id = repo.orders.get_max_id() + 1
            current_order = Order(order_id, order_location, hat_id)
            if hat_quantity == 1:
                repo.hats.remove(hat_id)
            else:
                repo.hats.decrease_quantity(hat_id)

            repo.orders.insert(current_order)
            order_supplier = repo.suppliers.findSupplierName(supplier)
            output.write(order_topping + "," + order_supplier + "," + order_location + "\n")


if __name__ == '__main__':
    main()

import mysql.connector
from bokeh.colors.groups import orange

from order import Order
from ordered_products import orderedProducts
from Models import *

# user=input("User: ")
# password=input("Password: ")

user = 'root'
password = 'Ahmed#123456789'
class DataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user=user,
            password=password,
            database="orders_database"
        )

        if self.db.is_connected():
            print("Connected Successfully")
        else:
            print("Failed to connect")

        self.cursor = self.db.cursor()

    def get_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        result = self.cursor.fetchall()
        orders = []
        for x in result:
            order_model = OrderModel(id=x[0], user_id=x[1], date=x[2],
                                     ordered_products=self.get_ordered_products(x[0]))
            orders.append(order_model)
        ans = []
        for o in orders:
            if not self.handle_no_products_order(o):
                ans.append(o)

        return ans

    def get_order_by_id(self, order_id):
        self.cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        x = self.cursor.fetchone()
        if x is not None:
            order_model = OrderModel(id=x[0], user_id=x[1], date=x[2],
                                     ordered_products=self.get_ordered_products(x[0]))
            return order_model
        else:
            return None

    def add_order(self, order):
        sql = "INSERT INTO orders (user_id, date) VALUES (%s, %s)"
        values = (order.user_id, order.date)
        self.cursor.execute(sql, values)
        order.id = self.cursor.lastrowid
        self.db.commit()
        for o in order.ordered_products:
            o.order_id = order.id
            self.add_product_to_order(o)
        self.handle_no_products_order(order)
        print("Order added successfully")
        return order.id

    def delete_order(self, id):
        sql = f"DELETE FROM ordered_products WHERE order_id = {id}"
        self.cursor.execute(sql)
        self.db.commit()
        sql = f"DELETE FROM orders WHERE id = {id}"
        self.cursor.execute(sql)
        self.db.commit()
        print("order deleted successfully")

    def update_order(self, order):
        sql = "UPDATE orders SET user_id = %s, date = %s WHERE id = %s"
        values = (order.user_id, order.date, order.id)
        self.cursor.execute(sql, values)
        self.db.commit()

        old_products = self.get_ordered_products(order.id)

        for o in order.ordered_products:
            if o not in old_products:
                self.add_product_to_order(o)

        for o in old_products:
            if o not in order.ordered_products:
                self.delete_ordered_product(o.product_id, o.order_id)

        self.handle_no_products_order(order)
        print("Order updated successfully")

    def add_product_to_order(self, ordered_product):
        sql = "INSERT INTO ordered_products (order_id, product_id, amount) VALUES (%s, %s, %s)"
        values = (ordered_product.order_id, ordered_product.product_id, ordered_product.amount)
        self.cursor.execute(sql, values)
        self.db.commit()
        print("Product added to order successfully")

    def delete_ordered_product(self, product_id, order_id):
        sql = "DELETE FROM ordered_products WHERE product_id = %s AND order_id = %s"
        values = (product_id, order_id)
        self.cursor.execute(sql, values)
        self.db.commit()
        order = self.get_order_by_id(order_id)
        self.handle_no_products_order(order)
        print("Ordered product deleted successfully")

    def get_ordered_products(self, order_id):
        sql = "SELECT * FROM ordered_products WHERE order_id = %s"
        values = (order_id,)
        self.cursor.execute(sql, values)
        result = self.cursor.fetchall()
        ordered_products = []
        for x in result:
            ordered_product = OrderedProductModel(order_id=x[0], product_id=x[1], amount=x[2])
            print(ordered_product)
            ordered_products.append(ordered_product)
        return ordered_products

    def update_ordered_product(self, ordered_product):
        sql = "UPDATE ordered_products SET amount = %s WHERE order_id = %s AND product_id = %s"
        values = (ordered_product.amount, ordered_product.order_id, ordered_product.product_id)
        self.cursor.execute(sql, values)
        self.db.commit()
        print("Ordered product updated successfully")

    def handle_no_products_order(self, order):
        if len(order.ordered_products) == 0:
            self.delete_order(order.id)
            return True
        return False

    def order_exist(self, order):
        orders = self.get_orders()
        for o in orders:
            if o == order and o.id == order.id:
                return True
        return False

    # def get_order_by_id(self, order_id):
    #     orders = self.get_orders()
    #     for o in orders:
    #         if o.id == order_id:
    #             return o
    #     return None

# d = DataBase()
# d.get_orders()
# d.get_ordered_products(4)
#
# product = orderedProducts(order_id=3, product_id=4, amount=2)
# d.add_product_to_order(product)

# order = Order(user_id=1, date='2024-05-05', status='Pending')
# d.add_order(order)
# d.add_order(order)
# d.add_order(order)
# d.add_order(order)

# existing_order = Order(user_id=1, date='2024-05-05', status='Delivered', id=2)
# d.update_order(existing_order)
# d.get_orders()

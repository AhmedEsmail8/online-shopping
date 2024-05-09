import mysql.connector
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
            database="products_database"
        )

        if self.db.is_connected():
            print("Connected Successfully")
        else:
            print("Failed to connect")

        self.cursor = self.db.cursor()

    # <editor-fold desc="products">
    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        result = self.cursor.fetchall()
        # products = []
        products_models = []
        for x in result:
            # product = Product(price=x[1], name=x[2], description=x[3], category=x[4], id=x[0])
            products_models.append(
                ProductModel(id=x[0], price=x[1], name=x[2], category=x[4], image=x[5], description=x[3], units=x[6]))
            # products.append(product)

        return products_models

    def add_product(self, product):
        sql = "INSERT INTO product (price, name, description, category, image, units) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (product.price, product.name, product.description, product.category, product.image, product.units)
        self.cursor.execute(sql, val)

        if self.cursor.rowcount > 0:
            print("Product inserted successfully")

            inserted_id = self.cursor.lastrowid
            print("Inserted ID:", inserted_id)
            self.db.commit()
            return inserted_id
        else:
            print("Failed to insert product")

    def delete_product(self, product_id):
        sql = f"DELETE FROM product WHERE id = {product_id}"
        self.cursor.execute(sql)
        self.db.commit()

    def update_product(self, product):
        query = "UPDATE product SET category=%s, description=%s, name=%s, price=%s, image=%s, units=%s WHERE id=%s"
        values = (product.category, product.description, product.name, product.price, product.image, product.units,
                  product.id)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("Product updated successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def is_product_exist(self, product):
        products = self.get_products()
        for p in products:
            if p == product:
                return True

        return False

    def get_product_by_id(self, product_id):
        products = self.get_products()
        for p in products:
            if p.id == product_id:
                return p

        return None

    # </editor-fold>




# d = DataBase()
# d.get_products()
# product = Product(price=180, name="white polo Tshirt", description="white polo Tshirt", category="men")
# image.id = d.add_image(image.file_location)
# product.id = d.add_product(product)
#
# d.add_image_to_product(8, 3)
#
# d.get_product_images(8)

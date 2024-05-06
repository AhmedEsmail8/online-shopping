import mysql.connector
from Models import *

# user=input("User: ")
# password=input("Password: ")
user = 'root'
password = 'yasmine123@'


class DataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user=user,
            password=password,
            database="online_shopping"
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
            images = self.get_product_images(x[0])
            images = [i[0] for i in images]
            products_models.append(
                ProductModel(id=x[0], price=x[1], name=x[2], category=x[4], images=images, description=x[3]))
            # products.append(product)

        return products_models

    def add_product(self, product):
        sql = "INSERT INTO product (price, name, description, category) VALUES (%s, %s, %s, %s)"
        val = (product.price, product.name, product.description, product.category)
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
        query = "UPDATE product SET category=%s, description=%s, name=%s, price=%s WHERE id=%s"
        values = (product.category, product.description, product.name, product.price, product.id)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("Product updated successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # </editor-fold>

    # <editor-fold desc="images">
    def add_image(self, file_location):
        sql = "INSERT INTO image (file_location) VALUES (%s)"
        val = [file_location]
        self.cursor.execute(sql, val)

        if self.cursor.rowcount > 0:
            print("image inserted successfully")

            inserted_id = self.cursor.lastrowid
            print("Inserted ID:", inserted_id)
            self.db.commit()
            return inserted_id
        else:
            print("Failed to insert image")

    def get_images(self):
        self.cursor.execute("SELECT * FROM image")
        result = self.cursor.fetchall()
        for x in result:
            print(x)
        return result

    def update_image(self, image):
        query = "UPDATE image SET file_location=%s WHERE id=%s"
        values = (image.file_location, image.id)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("image updated successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_image(self, image_id):
        sql = f"DELETE FROM image WHERE id = {image_id}"
        self.cursor.execute(sql)
        self.db.commit()

    # </editor-fold>

    def add_image_to_product(self, image_id, product_id):
        sql = "INSERT INTO product_images (product_id, image_id) VALUES (%s, %s)"
        val = (product_id, image_id)

        try:
            self.cursor.execute(sql, val)
            self.db.commit()
            print("image assigned to product successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_product_images(self, product_id):
        sql = "SELECT \
            image.file_location AS location \
            FROM product \
            INNER JOIN product_images ON product.id = product_images.product_id \
            INNER JOIN image ON product_images.image_id = image.id\
            WHERE product.id = %s "
        val = [product_id]
        self.cursor.execute(sql, val)

        result = self.cursor.fetchall()

        for x in result:
            print(x)

        return result

    def find_image(self, location):
        sql = "SELECT id FROM image WHERE file_location = %s"
        val = (location,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Image not found with the given location")
            return None


# d = DataBase()
# d.get_products()
# product = Product(price=180, name="white polo Tshirt", description="white polo Tshirt", category="men")
# image.id = d.add_image(image.file_location)
# product.id = d.add_product(product)
#
# d.add_image_to_product(8, 3)
#
# d.get_product_images(8)

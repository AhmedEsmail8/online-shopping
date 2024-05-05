import mysql.connector
from Product import Product
from Image import Image

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
            database="online_shopping"
        )

        if self.db.is_connected():
            print("Connected Successfully")
        else:
            print("Failed to connect")

        self.cursor = self.db.cursor()

    #<editor-fold desc="products">

    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        result = self.cursor.fetchall()
        for x in result:
            print(x)
        return result

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


    def delete_product(self, id):
        sql = f"DELETE FROM product WHERE id = {id}"
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

    #</editor-fold>

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

    def delete_image(self, id):
        sql = f"DELETE FROM image WHERE id = {id}"
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


d = DataBase()
# product = Product(price=180, name="white polo Tshirt", description="white polo Tshirt", category="men")
# image.id = d.add_image(image.file_location)
# product.id = d.add_product(product)
#
# d.add_image_to_product(8, 3)
#
# d.get_product_images(8)
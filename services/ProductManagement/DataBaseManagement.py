import sqlite3
from Models import *


class DataBase:
    def __init__(self):
        self.db = sqlite3.connect('products_database.db')
        self.cursor = self.db.cursor()

    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        result = self.cursor.fetchall()
        products_models = []
        for x in result:
            products_models.append(
                ProductModel(id=x[0], price=x[1], name=x[2], category=x[4], image=x[5], description=x[3], units=x[6])
            )
        return products_models

    def add_product(self, product):
        sql = """
            INSERT INTO product (price, name, description, category, image, units) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        val = (product.price, product.name, product.description, product.category, product.image, product.units)
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.lastrowid

    def delete_product(self, product_id):
        sql = "DELETE FROM product WHERE id = ?"
        self.cursor.execute(sql, (product_id,))
        self.db.commit()

    def update_product(self, product):
        query = """
            UPDATE product 
            SET category=?, description=?, name=?, price=?, image=?, units=? 
            WHERE id=?
        """
        values = (product.category, product.description, product.name, product.price, product.image, product.units,
                  product.id)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("Product updated successfully")
        except sqlite3.Error as err:
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


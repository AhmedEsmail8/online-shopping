import mysql.connector

class DataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Ahmed#123456789",
            database="online_shopping"
        )
        self.cursor = self.db.cursor()

    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        myresult = self.cursor.fetchall()
        for x in myresult:
            print(x)

d = DataBase()
d.get_products()
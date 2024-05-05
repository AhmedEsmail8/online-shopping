import mysql.connector

user=input("User: ")
password=input("Password: ")
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

    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        myresult = self.cursor.fetchall()
        for x in myresult:
            print(x)

d = DataBase()
d.get_products()
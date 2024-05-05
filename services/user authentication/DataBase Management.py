import mysql.connector
from user import User
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
            database="users_database"
        )

        if self.db.is_connected():
            print("Connected Successfully")
        else:
            print("Failed to connect")

        self.cursor = self.db.cursor()


    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        for x in result:
            print(x)
        return result

    def add_user(self, user):
        sql = "INSERT INTO users (first_name, last_name, age, email, password, mobile_number) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.age, user.email, user.password, user.mobile_number)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("User added successfully.")

    def delete_user(self, id):
        sql = f"DELETE FROM users WHERE id = {id}"
        self.cursor.execute(sql)
        self.db.commit()
        print("User deleted successfully.")

    def update_user(self, user):
        sql = "UPDATE users SET first_name = %s, last_name = %s, age = %s, email = %s, password = %s, mobile_number = %s WHERE id = %s"
        val = (user.first_name, user.last_name, user.age, user.email, user.password, user.mobile_number, user.id)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("User updated successfully.")

d = DataBase()
new_user = User("John", "Doe", 30, "john.doe@example.com", "password123", "1234567890")
d.add_user(new_user)
d.get_users()

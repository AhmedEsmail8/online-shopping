import sqlite3
from Models import *
# from user import User

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("users_database.db")
        self.cursor = self.db.cursor()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        users = []
        for x in result:
            user_model = UserModel(id=x[0], email=x[1], password=x[2], first_name=x[3], last_name=x[4], age=x[5],
                                   mobile_number=x[6], image=x[7], address=x[8])
            print(user_model)
            users.append(user_model)
        return users

    def add_user(self, user):
        sql = "INSERT INTO users (first_name, last_name, age, email, password, mobile_number, image, address)" \
              " VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        val = (user.first_name, user.last_name, user.age, user.email, user.password, user.mobile_number, user.image,
               user.address)
        self.cursor.execute(sql, val)
        inserted_id = self.cursor.lastrowid
        self.db.commit()
        print("User added successfully.")
        return inserted_id

    def delete_user(self, id):
        sql = "DELETE FROM users WHERE id = ?"
        self.cursor.execute(sql, (id,))
        self.db.commit()
        print("User deleted successfully.")

    def update_user(self, user):
        sql = "UPDATE users SET first_name = ?, last_name = ?, age = ?, email = ?, password = ?," \
              " mobile_number = ?, image = ?, address = ? WHERE id = ?"
        val = (user.first_name, user.last_name, user.age, user.email, user.password, user.mobile_number,
               user.image, user.address, user.id)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("User updated successfully.")

    def get_user_by_id(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result:
            user_model = UserModel(id=result[0], email=result[1], password=result[2], first_name=result[3],
                                   last_name=result[4], age=result[5], mobile_number=result[6], image=result[7],
                                   address=result[8])
            return user_model
        else:
            return None

    def is_email_exist(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

# Example usage:
# d = DataBase()
# d.delete_user(1)
# d.delete_user(2)
# d.delete_user(3)
# d.delete_user(4)
# user = User(email='john.doe@example.com', password='password123',
#             first_name='John', last_name='Doe', age=30,
#             mobile_number='1234567890', image='blablabla', address='Address')
# d.add_user(user)
# new_user = User("John", "Doe", 30, "john.doe@example.com",
#                 "password123", "1234567890", "blablabla", "Address")
# d.add_user(new_user)
# d.get_users()

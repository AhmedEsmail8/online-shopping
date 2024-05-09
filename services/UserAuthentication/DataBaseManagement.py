import mysql.connector
from Models import *
from user import User
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
            database="users_database"
        )

        if self.db.is_connected():
            print("Connected Successfully")
        else:
            print("Failed to connect")

        self.cursor = self.db.cursor()

    def get_users(self):
        self.db.close()
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user=user,
            password=password,
            database="users_database"
        )
        self.cursor = self.db.cursor()
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
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.age, user.email, user.password, user.mobile_number, user.image,
               user.address)
        self.cursor.execute(sql, val)
        inserted_id = self.cursor.lastrowid
        self.db.commit()
        print("User added successfully.")
        return inserted_id

    def delete_user(self, id):
        sql = f"DELETE FROM users WHERE id = {id}"
        self.cursor.execute(sql)
        self.db.commit()
        print("User deleted successfully.")

    def update_user(self, user):
        sql = "UPDATE users SET first_name = %s, last_name = %s, age = %s, email = %s, password = %s," \
              " mobile_number = %s, image = %s, address = %s WHERE id = %s"
        val = (user.first_name, user.last_name, user.age, user.email, user.password, user.mobile_number,
               user.image, user.address, user.id)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("User updated successfully.")

    def get_user_by_id(self, id):
        users = self.get_users()
        for user in users:
            if user.id==id:
                return user

        return None

    def is_email_exist(self, email):
        users = self.get_users()
        for user in users:
            if user.email == email:
                return True

        return False

# d = DataBase()
# d.delete_user(1)
# d.delete_user(2)
# d.delete_user(3)
# d.delete_user(4)

# user = User(email='john.doe@example.com', password='password123', first_name='John', last_name='Doe', age=30,
#                  mobile_number='1234567890', image='blablabla')
# d.add_user(user)
# new_user = User("John", "Doe", 30, "john.doe@example.com", "password123", "1234567890")
# d.add_user(new_user)
# d.add_user(new_user)
# d.add_user(new_user)
# d.add_user(new_user)
# d.get_users()

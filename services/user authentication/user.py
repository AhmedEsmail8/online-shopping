class User:
    def __init__(self, first_name, last_name, age, email, password, mobile_number, id=0):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.password = password
        self.mobile_number = mobile_number
        self.id = id

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}, Age: {self.age}, Email: {self.email}, " \
               f"Mobile Number: {self.mobile_number}, ID: {self.id}"

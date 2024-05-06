from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    email: str
    password: str
    first_name: str
    last_name: str
    age: int
    mobile_number: str

    def __str__(self):
        return f"ID: {self.id}, Email: {self.email}, Password: {self.password}, First Name: {self.first_name}," \
               f" Last Name: {self.last_name}, Age: {self.age}, Mobile Number: {self.mobile_number}"

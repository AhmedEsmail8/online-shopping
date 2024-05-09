from pydantic import BaseModel


class UserModel(BaseModel):
    id: int = -1
    email: str
    password: str
    first_name: str
    last_name: str
    age: int
    mobile_number: str
    image: str
    address: str

    def __str__(self):
        return f"ID: {self.id}, Email: {self.email}, Password: {self.password}, First Name: {self.first_name}," \
               f" Last Name: {self.last_name}, Age: {self.age}, Mobile Number: {self.mobile_number}, Image: {self.image}," \
               f"Address: {self.address}"

    def __eq__(self, other):
        if not isinstance(other, UserModel):
            return False
        return (
                # self.id == other.id and
                self.email == other.email and
                self.password == other.password and
                self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.age == other.age and
                self.mobile_number == other.mobile_number and
                self.image == other.image and
                self.address == other.address
        )

    def update_from(self, other):
        self.id = other.id
        self.email = other.email
        self.password = other.password
        self.first_name = other.first_name
        self.last_name = other.last_name
        self.age = other.age
        self.mobile_number = other.mobile_number
        self.image = other.image
        self.address = other.address

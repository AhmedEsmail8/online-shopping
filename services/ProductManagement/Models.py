from pydantic import BaseModel
from typing import List


class ProductModel(BaseModel):
    id: int = -1
    price: int
    name: str
    category: str
    description: str
    image: str
    units: int = 0

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Price: {self.price}," \
               f" Category: {self.category}, Description: {self.description}, Image: {self.image}," \
               f" Units: {self.units}"

    def __eq__(self, other):
        if not isinstance(other, ProductModel):
            return False
        return (
                # self.id == other.id and
                self.price == other.price and
                self.name == other.name and
                self.category == other.category and
                self.description == other.description and
                self.image == other.image and
                self.units == other.units
        )


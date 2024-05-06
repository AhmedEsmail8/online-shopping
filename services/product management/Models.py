from pydantic import BaseModel
from typing import List


class ProductModel(BaseModel):
    id: int
    price: int
    name: str
    category: str
    description: str
    images: List[str]

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Price: {self.price}," \
               f" Category: {self.category}, Description: {self.description}, Images: {self.images}"

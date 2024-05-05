import Image

class Product:
    def __init__(self, price, name, description, category, id=0):
        self.price = price
        self.name = name
        self.description = description
        self.category = category
        self.product_images = []
        self.id = id

    def __str__(self):
        return f"Product ID: {self.id}\nName: {self.name}\nCategory: {self.category}\nPrice: {self.price}\nDescription: " \
               f"{self.description}\nImages: {self.product_images}"
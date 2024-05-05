import Image

class Product:
    def __init__(self, price, name, description, category, id=0):
        self.price = price
        self.name = name
        self.description = description
        self.category = category
        self.product_images = []
        self.id = id

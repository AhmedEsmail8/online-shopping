class Product:
    def __init__(self, price, name, description, category, product_image, id=0):
        self.price = price
        self.name = name
        self.description = description
        self.category = category
        self.image = product_image
        self.id = id

    def __str__(self):
        return f"Product ID: {self.id}\nName: {self.name}\nCategory: {self.category}\n" \
               f"Price: {self.price}\nDescription: " \
               f"{self.description}\nImages: {self.image}"

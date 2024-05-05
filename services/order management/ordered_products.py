class orderedProducts:
    def __init__(self, order_id, product_id, amount):
        self.order_id = order_id
        self.product_id = product_id
        self.amount = amount

    def __str__(self):
        return f"Order ID: {self.order_id}, Product ID: {self.product_id}, Amount: {self.amount}"

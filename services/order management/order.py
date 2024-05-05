class Order:
    def __init__(self, user_id, date, status, id=0):
        self.user_id = user_id
        self.date = date
        self.status = status
        self.id = id

    def __str__(self):
        return f"Order ID: {self.id}, User ID: {self.user_id}, Date: {self.date}, Status: {self.status}"

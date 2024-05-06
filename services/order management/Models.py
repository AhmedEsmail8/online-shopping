from pydantic import BaseModel
from datetime import datetime


class OrderModel(BaseModel):
    id: int
    user_id: int
    date: datetime
    status: str

    def __str__(self):
        return f"Order ID: {self.id}, User ID: {self.user_id}, Date: {self.date}, Status: {self.status}"


class OrderedProductModel(BaseModel):
    order_id: int
    product_id: int
    amount: int

    def __str__(self):
        return f"Order ID: {self.order_id}, Product ID: {self.product_id}, Amount: {self.amount}"

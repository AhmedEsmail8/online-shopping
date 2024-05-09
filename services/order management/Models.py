from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List


class OrderedProductModel(BaseModel):
    order_id: int = -1
    product_id: int
    amount: int

    def __str__(self):
        return f"Order ID: {self.order_id}, Product ID: {self.product_id}, Amount: {self.amount}"

    def __eq__(self, other):
        if not isinstance(other, OrderedProductModel):
            return False
        return (
            self.order_id == other.order_id and
            self.product_id == other.product_id
            and self.amount == other.amount
        )


class OrderModel(BaseModel):
    id: int = -1
    user_id: int
    date: datetime
    ordered_products: List[OrderedProductModel]

    def __str__(self):
        return f"Order ID: {self.id}, User ID: {self.user_id}, Date: {self.date}," \
               f" Ordered Products: {self.ordered_products}"

    def __eq__(self, other):
        if not isinstance(other, OrderModel):
            return False

        equal_lists = True

        for ordered_product in self.ordered_products:
            if ordered_product not in other.ordered_products:
                equal_lists = False
                break

        for ordered_product in other.ordered_products:
            if ordered_product not in self.ordered_products:
                equal_lists = False
                break

        return (
            # self.id == other.id and
            self.user_id == other.user_id
            and self.date == other.date
            and equal_lists
        )

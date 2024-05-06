from fastapi import FastAPI
from DataBaseManagement import DataBase
import uvicorn
from Models import *

app = FastAPI()
d = DataBase()

@app.get("/")
async def get_orders():
    return d.get_orders()

@app.post("/")
async def add_order(item: OrderModel):
    return d.add_order(item)

@app.put("/")
async def update_order(item: OrderModel):
    return d.update_order(item)

@app.delete("/")
async def delete_order(item_id: int):
    return d.delete_order(item_id)

@app.get("/{order_id}")
async def get_ordered_products(order_id):
    return d.get_ordered_products(order_id)

# @app.post("/")
# async def add_product_to_order(item: OrderedProductModel):
#     return d.add_product_to_order(item)
#
# @app.put("/")
# async def update_ordered_product(item: OrderedProductModel):
#     return d.update_ordered_product(item)

@app.delete("/{product_id}")
async def delete_ordered_product(item_id: int):
    return d.delete_ordered_product(item_id)

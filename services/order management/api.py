from fastapi import FastAPI, HTTPException
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
    if d.order_exist(item):
        raise HTTPException(status_code=400, detail="order already exists")
    return d.add_order(item)


@app.put("/")
async def update_order(item: OrderModel):
    if d.get_order_by_id(item.id) is None:
        raise HTTPException(status_code=404, detail="order not found")
    return d.update_order(item)


@app.delete("/")
async def delete_order(item_id: int):
    if d.get_order_by_id(item_id) is None:
        raise HTTPException(status_code=404, detail="order not found")
    return d.delete_order(item_id)


@app.get("/{order_id}")
async def get_ordered_products(order_id):
    if d.get_order_by_id(order_id) is None:
        raise HTTPException(status_code=404, detail="order not found")
    return d.get_ordered_products(order_id)

# @app.post("/")
# async def add_product_to_order(item: OrderedProductModel):
#     return d.add_product_to_order(item)
#
# @app.put("/")
# async def update_ordered_product(item: OrderedProductModel):
#     return d.update_ordered_product(item)


@app.delete("/{order_id}")
async def delete_ordered_product(order_id, product_id: int):
    if d.get_order_by_id(order_id) is None:
        raise HTTPException(status_code=404, detail="order not found")
    return d.delete_ordered_product(product_id, order_id)

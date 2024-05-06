from fastapi import FastAPI
from DataBaseManagement import DataBase
import uvicorn
from Models import *

app = FastAPI()
d = DataBase()


@app.get("/")
async def get_items():
    return d.get_products()


@app.post("/")
async def add_product(item: ProductModel):
    return d.add_product(item)


@app.put("/")
async def update_product(item: ProductModel):
    return d.update_product(item)


@app.delete("/")
async def delete_product(item_id: int):
    return d.delete_product(item_id)

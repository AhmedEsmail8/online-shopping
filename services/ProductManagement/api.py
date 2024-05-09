from fastapi import FastAPI, HTTPException
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
    if d.is_product_exist(item):
        raise HTTPException(status_code=400, detail="Product already exists")
    inserted_id = d.add_product(item)
    item.id = inserted_id
    return item.dict()


@app.put("/")
async def update_product(item: ProductModel):
    if d.is_product_exist(item):
        raise HTTPException(status_code=400, detail="Product already exists")
    if d.get_product_by_id(item.id) is None:
        raise HTTPException(status_code=404, detail="product not found")
    d.update_product(item)
    return item.dict()


@app.delete("/")
async def delete_product(item_id: int):
    if d.get_product_by_id(item_id) is None:
        raise HTTPException(status_code=404, detail="product not found")
    d.delete_product(item_id)
    return {"message": "Product deleted"}

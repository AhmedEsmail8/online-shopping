from fastapi import FastAPI
from DataBaseManagement import DataBase
import uvicorn
from Models import *

app = FastAPI()
d = DataBase()


@app.get("/")
async def get_orders():
    return d.get_orders()


@app.get("/{order_id}")
async def get_ordered_products(order_id):
    return d.get_ordered_products(order_id)


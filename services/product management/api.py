from fastapi import FastAPI
from DataBaseManagement import DataBase
import uvicorn
from Models import *

app = FastAPI()
d = DataBase()

db = d.get_products()


@app.get("/")
async def get_items():
    return db

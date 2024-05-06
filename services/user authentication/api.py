from fastapi import FastAPI
from DataBaseManagement import DataBase
from Models import *


app = FastAPI()
d = DataBase()

@app.get("/")
async def get_users():
    return d.get_users()


@app.post("/")
async def add_user(item: UserModel):
    return d.add_user(item)


@app.put("/")
async def update_user(item: UserModel):
    return d.update_user(item)


@app.delete("/")
async def delete_user(item_id: int):
    return d.delete_user(item_id)

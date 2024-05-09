from fastapi import FastAPI, HTTPException
from DataBaseManagement import DataBase
from Models import *


app = FastAPI()
d = DataBase()


@app.get("/")
async def get_users():
    return d.get_users()


@app.post("/")
async def add_user(user: UserModel):
    if d.is_email_exist(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return d.add_user(user)


@app.put("/")
async def update_user(user: UserModel):
    if d.get_user_by_id(user.id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if d.get_user_by_id(user.id).email != user.email and d.is_email_exist(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return d.update_user(user)


@app.delete("/")
async def delete_user(user_id: int):
    if d.get_user_by_id(user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return d.delete_user(user_id)

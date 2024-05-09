import requests as req
from fastapi import FastAPI, HTTPException
from Models import *
# from services.UserAuthentication import DataBaseManagement as user_database
import json

# The API endpoint
order_management_url = "http://127.0.0.1:8080"
product_management_url = "http://127.0.0.1:3000"
user_url = "http://127.0.0.1:8001"

app = FastAPI()


class HelperFunctions:

    # <editor-fold desc="User">
    @staticmethod
    def user_email_exist(email):
        users = req.get(user_url).json()
        for u in users:
            if u['email'] == email:
                return True
        return False

    @staticmethod
    def get_user_by_id(user_id):
        users = req.get(user_url).json()
        for u in users:
            if u['id'] == user_id:
                return u
        return None
    # </editor-fold>

@app.get("/login")
async def get_users():
    return req.get(user_url).json()


@app.post("/register")
async def add_user(user: UserModel):
    if HelperFunctions.user_email_exist(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return req.post(user_url, json=user.dict()).json()


@app.put("/{user_id}/profile")
async def update_user(user_id, user: UserModel):
    user.id = user_id
    if HelperFunctions.get_user_by_id(user.id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if HelperFunctions.get_user_by_id(user.id)['email'] != user.email and HelperFunctions.user_email_exist(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return req.put(user_url, json=user.dict()).json()


@app.delete("/{user_id}/profile")
async def delete_user(user_id):
    data = {'user_id': user_id}
    return req.delete(user_url, params=data).json()


@app.get("/{user_id}/home")
@app.get("/admin/products")
async def get_products():
    return req.get(product_management_url).json()


@app.post("/admin/add product")
async def add_product(item: ProductModel):
    return req.post(product_management_url, json=item.dict()).json()


@app.delete("/admin/products")
async def delete_product(product_id: int):
    data = {"item_id": product_id}
    return req.delete(product_management_url, params=data).json()


@app.put("/admin/update product")
async def update_product(item: ProductModel):
    return req.put(product_management_url, json=item.dict()).json()


@app.get("/admin/orders")
async def get_orders():
    return req.get(order_management_url).json()


@app.post("/{user_id}/cart")
async def add_order(user_id, order: OrderModel):
    order.user_id = user_id
    order.date = order.date.isoformat()
    return req.post(order_management_url, json=order.dict()).json()


@app.put("/{user_id}/orders/{order_id}")
async def update_order(user_id, order_id, order: OrderModel):
    order.user_id = user_id
    order.id = order_id
    order.date = order.date.isoformat()
    return req.put(order_management_url, json=order.dict()).json()


@app.delete("/admin/orders")
async def delete_order(order_id: int):
    data = {"item_id": order_id}
    return req.delete(order_management_url, params=data).json()


@app.get("/{user_id}/orders/{order_id}")
async def get_ordered_products(user_id, order_id):
    return req.get(f"{order_management_url}/{order_id}").json()


@app.delete("/{user_id}/orders/{order_id}")
async def delete_ordered_products(user_id, order_id, product_id: int):
    data = {"item_id": product_id}
    return req.delete(f"{order_management_url}/{order_id}", params=data).json()


# @app.get("/{user_id}/orders")
# @app.get("/admin/orders")
# async def get_orders():
#     return req.get(order_management_url).json()

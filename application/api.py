import requests as req
from fastapi import FastAPI, HTTPException
from Models import *

# The API endpoint
order_management_url = "http://order-service:8080"
product_management_url = "http://product-service:3030"
user_url = "http://user-service:8001"

app = FastAPI()


class HelperFunctions:

    @staticmethod
    def get_user_by_id(user_id):
        users = req.get(user_url).json()
        for u in users:
            if u['id'] == user_id:
                return u
        return None

    @staticmethod
    def get_product_by_id(product_id):
        products = req.get(product_management_url).json()
        for product in products:
            if product['id'] == product_id:
                return product
        return None

    @staticmethod
    def get_order_by_id(product_id):
        orders = req.get(order_management_url).json()
        for order in orders:
            if order['id'] == product_id:
                return order
        return None


@app.get("/")
async def get_users():
    return req.get(user_url).json()


@app.post("/login")
async def login(email: str, password: str):
    users = req.get(user_url).json()
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user
    raise HTTPException(status_code=401, detail="Invalid email or password")


@app.post("/register")
async def add_user(user: UserModel):
    return req.post(user_url, json=user.dict()).json()


@app.put("/{user_id}/profile")
async def update_user(user_id, user: UserModel):
    user.id = user_id
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
    if HelperFunctions.get_user_by_id(int(user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found")
    for product in order.ordered_products:
        if HelperFunctions.get_product_by_id(product.product_id) is None:
            raise HTTPException(status_code=404, detail="product not found")

    order.user_id = user_id
    order.date = order.date.isoformat()
    return req.post(order_management_url, json=order.dict()).json()


@app.put("/{user_id}/orders/{order_id}")
async def update_order(user_id, order_id, order: OrderModel):
    order.user_id = user_id
    order.id = order_id
    for product in order.ordered_products:
        product.order_id = order_id

    if HelperFunctions.get_user_by_id(int(user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if HelperFunctions.get_order_by_id(int(order_id)) is None:
        raise HTTPException(status_code=404, detail="order not found")
    for product in order.ordered_products:
        if HelperFunctions.get_product_by_id(product.product_id) is None:
            raise HTTPException(status_code=404, detail="product not found")

    order.date = order.date.isoformat()
    return req.put(order_management_url, json=order.dict()).json()


@app.delete("/admin/orders")
async def delete_order(order_id: int):
    data = {"item_id": order_id}
    return req.delete(order_management_url, params=data).json()


@app.get("/{user_id}/orders/{order_id}")
async def get_ordered_products(user_id, order_id):
    if HelperFunctions.get_user_by_id(int(user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if HelperFunctions.get_order_by_id(int(order_id)) is None:
        raise HTTPException(status_code=404, detail="order not found")
    return req.get(f"{order_management_url}/{order_id}").json()


@app.delete("/{user_id}/orders/{order_id}")
async def delete_ordered_products(user_id, order_id, product_id: int):
    if HelperFunctions.get_user_by_id(int(user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if HelperFunctions.get_order_by_id(int(order_id)) is None:
        raise HTTPException(status_code=404, detail="order not found")
    if HelperFunctions.get_product_by_id(int(product_id)) is None:
        raise HTTPException(status_code=404, detail="product not found")
    data = {"item_id": product_id}
    return req.delete(f"{order_management_url}/{order_id}", params=data).json()

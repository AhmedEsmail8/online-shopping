import unittest
from fastapi.testclient import TestClient
from api import *

orders = d.get_orders()
for order in orders:
    d.delete_order(order.id)

order_id = -1


class TestAppEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_add_order(self):
        before_adding = len(d.get_orders())

        sample_product = OrderedProductModel(product_id=1, amount=5)
        sample_order = OrderModel(user_id=1, date="2024-05-09T12:00:00", ordered_products=[sample_product])
        sample_order.date = sample_order.date.isoformat()
        response = self.client.post("/", json=sample_order.dict())
        self.assertEqual(response.status_code, 200)

        after_adding = len(d.get_orders())
        self.assertEqual(after_adding, before_adding+1)

    def test_add_existing_order(self):
        sample_product = OrderedProductModel(product_id=2, amount=20)
        sample_order = OrderModel(user_id=3, date="2024-05-09T12:00:00", ordered_products=[sample_product])
        d.add_order(sample_order)

        before_adding = len(d.get_orders())
        sample_order.date = sample_order.date.isoformat()
        response = self.client.post("/", json=sample_order.dict())
        self.assertEqual(response.status_code, 400)

        after_adding = len(d.get_orders())
        self.assertEqual(after_adding, before_adding)

    def test_get_orders(self):
        global order_id
        orders = d.get_orders()
        for order in orders:
            d.delete_order(order.id)

        sample_product = OrderedProductModel(product_id=1, amount=5)
        sample_order = OrderModel(user_id=1, date="2024-05-09T12:00:00", ordered_products=[sample_product])

        order_id = d.add_order(sample_order)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        orders = d.get_orders()
        found = False
        for o in orders:
            if o == sample_order:
                found = True

        self.assertTrue(found)

    def test_update_order(self):
        global order_id

        sample_product = OrderedProductModel(order_id=order_id, product_id=1, amount=5)
        sample_product2 = OrderedProductModel(order_id=order_id, product_id=2, amount=3)
        sample_order = OrderModel(id=order_id, user_id=1, date="2024-05-09T12:00:00", ordered_products=[sample_product, sample_product2])
        sample_order.date = sample_order.date.isoformat()

        response = self.client.put("/", json=sample_order.dict())
        self.assertEqual(response.status_code, 200)

        orders = d.get_orders()
        found = False
        for o in orders:
            o.date = o.date.isoformat()
            if o == sample_order:
                found = True
                break
        self.assertTrue(found)

    def test_update_order_2(self):
        global order_id
        sample_order = OrderModel(id=order_id, user_id=1, date="2024-05-09T12:00:00",
                                  ordered_products=[])
        sample_order.date = sample_order.date.isoformat()

        response = self.client.put("/", json=sample_order.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(d.get_orders()), 0)

    def test_update_not_existing_order(self):
        sample_product = OrderedProductModel(product_id=2, amount=20)
        sample_order = OrderModel(user_id=-1, date="2024-05-09T12:00:00",
                                  ordered_products=[sample_product])
        sample_order.date = sample_order.date.isoformat()

        response = self.client.put("/", json=sample_order.dict())
        self.assertEqual(response.status_code, 404)

    def test_delete_order(self):
        sample_product = OrderedProductModel(product_id=1, amount=5)
        sample_order = OrderModel(user_id=1, date="2024-05-09T12:00:00", ordered_products=[sample_product])

        order_id = d.add_order(sample_order)
        before_adding = len(d.get_orders())
        response = self.client.delete("/", params={"item_id": order_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(d.get_orders()), before_adding-1)

    def test_delete_not_existing_order(self):
        before_adding = len(d.get_orders())
        response = self.client.delete("/", params={"item_id": -1})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(d.get_orders()), before_adding)

    def test_get_ordered_products(self):
        sample_product = OrderedProductModel(product_id=1, amount=5)
        sample_order = OrderModel(user_id=1, date="2024-05-09T12:00:00", ordered_products=[sample_product])
        order_id = d.add_order(sample_order)
        response = self.client.get(f"/{order_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [sample_product.dict()])

    def test_get_ordered_products_2(self):
        response = self.client.get(f"/{-1}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'order not found'})

    def test_delete_ordered_product(self):
        sample_product1 = OrderedProductModel(product_id=1, amount=5)
        sample_product2 = OrderedProductModel(product_id=3, amount=7)
        sample_order = OrderModel(user_id=1, date="2024-05-09T12:00:00", ordered_products=[sample_product1, sample_product2])
        order_id = d.add_order(sample_order)
        response = self.client.delete(f"/{order_id}", params={"product_id": 1})
        self.assertEqual(response.status_code, 200)
        order = d.get_order_by_id(order_id)
        self.assertEqual(order.ordered_products, [sample_product2])

    def test_delete_ordered_product_2(self):
        response = self.client.delete(f"/{-1}", params={"product_id": 1})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'order not found'})

    #
    # # Uncomment these tests once the corresponding endpoints are implemented
    # """
    # def test_add_product_to_order(self):
    #     response = client.post("/", json=sample_product.dict())
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions as needed
    #
    # def test_update_ordered_product(self):
    #     response = client.put("/", json=sample_product.dict())
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions as needed
    # """
    #



if __name__ == "__main__":
    unittest.main()

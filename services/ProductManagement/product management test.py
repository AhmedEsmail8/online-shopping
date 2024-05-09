import unittest
from fastapi.testclient import TestClient
from api import *


products = d.get_products()
for p in products:
    d.delete_product(p.id)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_add_product(self):
        before_adding = len(d.get_products())
        product = ProductModel(price=100, name='White Polo Tshirt', category='men',
                               description='White coton Polo Tshirt', units=70,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        response = self.client.post("/", json=product.dict())
        self.assertEqual(response.status_code, 200)
        after_adding = len(d.get_products())
        self.assertEqual(after_adding, before_adding+1)

    def test_get_products(self):
        products = d.get_products()
        for p in products:
            d.delete_product(p.id)
        product = ProductModel(price=100, name='White Polo Tshirt', category='men',
                               description='White coton Polo Tshirt', units=70,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        d.add_product(product)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_add_existing_product(self):

        product = ProductModel(price=100, name='White shirt', category='men',
                               description='White shirt', units=70,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        d.add_product(product)

        before_adding = len(d.get_products())
        product = ProductModel(price=100, name='White shirt', category='men',
                               description='White shirt', units=70,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        response = self.client.post("/", json=product.dict())
        self.assertEqual(response.status_code, 400)
        after_adding = len(d.get_products())
        self.assertEqual(after_adding, before_adding)

    def test_update_product(self):
        product = ProductModel(price=100, name='black shoes', category='women',
                               description='black shoes', units=20,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        product_id = d.add_product(product)
        product.id = product_id

        product.name = 'red shoes'
        product.description = 'red shoes'

        response = self.client.put("/", json=product.dict())
        self.assertEqual(response.status_code, 200)

        products = d.get_products()
        found = False

        for p in products:
            if p == product and p.id == product.id:
                found = True
                break

        self.assertTrue(found)

    def test_update_product_to_existing(self):
        product = ProductModel(price=100, name='black shoes', category='women',
                               description='black shoes', units=20,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        product_id = d.add_product(product)
        product.id = product_id

        product.name = 'red shoes'
        product.description = 'red shoes'

        response = self.client.put("/", json=product.dict())
        self.assertEqual(response.status_code, 400)

    def test_update_not_found_product(self):
        product = ProductModel(price=100, name='ice cap', category='men',
                               description='ice cap', units=15,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")

        response = self.client.put("/", json=product.dict())
        self.assertEqual(response.status_code, 404)

        found = False
        products = d.get_products()
        for p in products:
            if p == product:
                found = True
                break
        self.assertFalse(found)

    def test_delete_product(self):
        product = ProductModel(price=100, name='ice cap', category='men',
                               description='ice cap', units=15,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")
        product_id = d.add_product(product)
        product.id = product_id
        before_deleting = len(d.get_products())
        response = self.client.delete("/", params={"item_id": product_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Product deleted"})
        after_deleting = len(d.get_products())
        self.assertEqual(after_deleting, before_deleting - 1)

    def test_delete_not_found_product(self):
        product = ProductModel(price=100, name='ice cap', category='men',
                               description='ice cap', units=15,
                               image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg")

        before_deleting = len(d.get_products())
        response = self.client.delete("/", params={"item_id": product.id})
        self.assertEqual(response.status_code, 404)

        after_deleting = len(d.get_products())
        self.assertEqual(after_deleting, before_deleting)


if __name__ == "__main__":
    unittest.main()

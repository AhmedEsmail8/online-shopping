import unittest
from fastapi.testclient import TestClient
from api import *


users = d.get_users()
for i in users:
    d.delete_user(i.id)


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_add_user(self):
        before_adding = len(d.get_users())
        new_user = UserModel(email='john.doe@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")

        response = self.client.post("/", json=new_user.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(d.get_users()), before_adding+1)

        user = d.get_users()[0]
        new_user.id = user.id
        self.assertEqual(user, new_user)

        print(len(d.get_users()))

    def test_get_users(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        new_user = UserModel(email='john.doe1@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")
        d.add_user(new_user)
        new_user.email = 'john.doe2@example.com'
        d.add_user(new_user)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_update_user(self):
        user = UserModel(email='john.doe3@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")
        user_id = d.add_user(user)
        user.id = user_id

        user.first_name = 'Ahmed'
        user.last_name = "Esmail"

        response = self.client.put("/", json=user.dict())
        self.assertEqual(response.status_code, 200)

        users = d.get_users()
        found = False

        for u in users:
            if u.id == user.id:
                self.assertEqual(u, user)
                found = True
                break

        self.assertTrue(found)

    def test_update_not_found_user(self):
        user = UserModel(email='john.doe4@example.com', password='password123', first_name='Fname',
                             last_name='Lname', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")


        response = self.client.put("/", json=user.dict())
        self.assertEqual(response.status_code, 404)

        users = d.get_users()
        found = False

        for u in users:
            if u.id == user.id:
                self.assertEqual(u, user)
                found = True
                break

        self.assertFalse(found)

    def test_delete_user(self):
        new_user = UserModel(email='john.doe5@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")
        user_id = d.add_user(new_user)
        before_deleting = len(d.get_users())
        response = self.client.delete(f"/?user_id={user_id}")
        self.assertEqual(response.status_code, 200)
        after_deleting = len(d.get_users())
        self.assertEqual(after_deleting, before_deleting-1)

    def test_delete_not_found_user(self):
        new_user = UserModel(email='john.doe6@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")
        before_deleting = len(d.get_users())
        response = self.client.delete(f"/?user_id={new_user.id}")
        self.assertEqual(response.status_code, 404)
        after_deleting = len(d.get_users())
        self.assertEqual(after_deleting, before_deleting)

    def test_add_user_with_existing_email(self):
        before_adding = len(d.get_users())
        new_user = UserModel(email='john.doe@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")

        response = self.client.post("/", json=new_user.dict())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(d.get_users()), before_adding)

    def test_update_user_with_existing_email(self):
        user = UserModel(email='john.doe5132@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")

        user2 = UserModel(email='john.doe123@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")

        user_id = d.add_user(user)
        user.id = user_id

        user2_id = d.add_user(user2)
        user2.id = user2_id

        user2.email = user.email

        response = self.client.put("/", json=user2.dict())
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()

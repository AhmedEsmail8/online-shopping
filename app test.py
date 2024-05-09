import unittest
from fastapi.testclient import TestClient
from api import *



class AppTest(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_get_users(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    # make sure the email not added before in the database
    def test_add_user(self):
        new_user = UserModel(email='john@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")
        users_before = self.client.get('/login').json()
        response = self.client.post('/register', json=new_user.dict())
        self.assertEqual(response.status_code, 200)
        users_after = self.client.get('/login').json()
        self.assertEqual(len(users_before), len(users_after)-1)

    def test_add_existing_user_email(self):
        new_user = UserModel(email='john1@example.com', password='password123', first_name='John',
                             last_name='Doe', age=30, mobile_number='1234567890',
                             image="C:/Users/Lenovo/Desktop/WhatsApp Image 2024-02-17 at 14.52.38_c8f08752.jpg",
                             address="4 Nour Al Nems St, AL Haram, Giza")
        add_response = self.client.post('/register', json=new_user.dict())

        users_before = self.client.get('/login').json()
        response = self.client.post('/register', json=new_user.dict())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Email already exists'})
        users_after = self.client.get('/login').json()
        self.assertEqual(len(users_before), len(users_after))


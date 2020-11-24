import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapp.models import Category

class CategoryTests(APITestCase):
    def setUp(self):
        """
        Create a new account, and a default category
        """
        url = "/register"
        data = {
            "username": "jweckert17",
            "password": "hunter2",
            "email": "jweckert17@gmail.com",
            "first_name": "Jacob",
            "last_name": "Eckert",
            "bio": "Cool boi"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.token = json_response["token"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = Category(name="Strategy")
        category.save()
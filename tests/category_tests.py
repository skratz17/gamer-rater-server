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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        category = Category(name="Strategy")
        category.save()

    def test_get_existing_category(self):
        """
        Test getting a single category by ID that should exist.
        """
        response = self.client.get("/categories/1")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["name"], "Strategy")

    def test_get_nonexisting_category(self):
        """
        Test getting a single category by ID that should not exist.
        """
        response = self.client.get("/categories/69")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_categories(self):
        """
        Test getting all categories.
        """
        response = self.client.get("/categories")
        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]["id"], 1)
        self.assertEqual(json_response[0]["name"], "Strategy")

        category = Category(name="Action")
        category.save()

        response = self.client.get("/categories")
        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["id"], 1)
        self.assertEqual(json_response[0]["name"], "Strategy")
        self.assertEqual(json_response[1]["id"], 2)
        self.assertEqual(json_response[1]["name"], "Action")
import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapp.models import Designer

class DesignerTests(APITestCase):
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

    def test_get_all_designers(self):
        """
        Test getting all designers.
        """

        # Test getting list of designers with none in DB.
        response = self.client.get("/designers")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 0)

        # Create two designers and save in DB.
        designer = Designer(name="John Designer")
        designer.save()

        designer = Designer(name="Bob Designer")
        designer.save()

        # Test getting list of designers with two in DB.
        response = self.client.get("/designers")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 2)

        self.assertEqual(json_response[0]["id"], 1)
        self.assertEqual(json_response[0]["name"], "John Designer")

        self.assertEqual(json_response[1]["id"], 2)
        self.assertEqual(json_response[1]["name"], "Bob Designer")

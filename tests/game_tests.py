import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapp.models import Game, Category, Designer

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account, and a default category and designer
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

        designer = Designer(name="Firaxis")
        designer.save()

    def test_create_valid_game(self):
        """
        Test creating a game with correct values in request.
        """

        # Create the valid game
        url = "/games"
        data = {
            "title": "Civ VI",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1,
            "categories": [ 1 ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/games/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)

        self.assertEqual(json_response["title"], "Civ VI")
        self.assertEqual(json_response["description"], "This fun game")
        self.assertEqual(json_response["year"], 2016)
        self.assertEqual(json_response["num_players"], 12)
        self.assertEqual(json_response["estimated_duration"], 300)
        self.assertEqual(json_response["age_recommendation"], 13)
        self.assertEqual(json_response["designer"]["id"], 1)
        self.assertEqual(len(json_response["categories"]), 1)
        self.assertEqual(json_response["categories"][0]["id"], 1)

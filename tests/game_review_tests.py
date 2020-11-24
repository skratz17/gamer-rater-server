import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from raterapp.models import GameReview, Game, Designer

class GameReviewTests(APITestCase):
    def setUp(self):
        """
        Create a new account, and a default game
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

        designer = Designer(name="Firaxis")
        designer.save()

        game = Game(
            title="Civ VI", description="This fun game", year=2016,
            num_players=12, estimated_duration=300, age_recommendation=13, designer_id=1
        )
        game.save()

    def test_create_valid_game_review(self):
        data = {
            "gameId": 1,
            "rating": 9,
            "review": "a romp",
            "timestamp": "2020-11-20 17:50:37.451000"
        }

        response = self.client.post("/reviews", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # verify that the review saved to DB matches the request
        review = GameReview.objects.get(pk=1)

        self.assertEqual(review.game.id, 1)
        self.assertEqual(review.rating, 9)
        self.assertEqual(review.review, "a romp")

        thisDatetime = datetime.datetime.fromisoformat("2020-11-20 17:50:37.451000")
        self.assertEqual(datetime.datetime.timestamp(thisDatetime), datetime.datetime.timestamp(review.timestamp))

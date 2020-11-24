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
        """
        Test creating a valid game review
        """

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

    def test_create_game_review_with_missing_required_property(self):
        """
        Test creating a game without a required PUT body property
        """

        # missing required timestamp property
        data = {
            "gameId": 1,
            "rating": 9,
            "review": "a romp"
        }

        response = self.client.post("/reviews", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_game_review_for_nonexistent_game(self):
        """
        Test creating a game review for an invalid game id
        """

        data = {
            "gameId": 666,
            "rating": 9,
            "review": "a romp",
            "timestamp": "2020-11-20 17:50:37.451000"
        }

        response = self.client.post("/reviews", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_game_reviews(self):
        """
        Get all game reviews
        """
        self._seed_game_reviews()

        response = self.client.get('/reviews')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["review"], "a romp")
        self.assertEqual(json_response[1]["review"], "a whirlwind")

    def test_get_game_reviews_for_single_game(self):
        """
        Get all game reviews for game id of 1, and then for a nonexistent game id
        """
        self._seed_game_reviews()

        response = self.client.get('/reviews?gameId=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["review"], "a romp")
        self.assertEqual(json_response[1]["review"], "a whirlwind")

        response = self.client.get('/reviews?gameId=666')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 0)

    def _seed_game_reviews(self):
        """
        Save two game reviews in the DB
        """
        review = GameReview(
            game_id= 1,
            player_id=1,
            rating= 9,
            review= "a romp",
            timestamp= "2020-11-20 17:50:37.451000" 
        )
        review.save()

        review = GameReview(
            game_id= 1,
            player_id=1,
            rating= 8,
            review= "a whirlwind",
            timestamp= "2020-11-20 17:50:37.451000" 
        )
        review.save()
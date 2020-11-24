import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapp.models import Game, Category, GameCategory, Designer

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account, three default categories, and a designer
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

        category = Category(name="Sports")
        category.save()

        category = Category(name="RPG")
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

    def test_create_game_with_missing_required_property(self):
        """
        Test creating a game that is missing a required property in request body.
        """

        url = "/games"

        # "title" property not included
        data = {
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1,
            "categories": [ 1 ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_game_with_invalid_category_id(self):
        """
        Test creating a game that includes invalid category ids in categories array
        """

        url = "/games"
        data = {
            "title": "Civ VI",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1,
            "categories": [ 1, 666 ] # category id of 666 is invalid
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_game_with_invalid_designer_id(self):
        """
        Test creating a game that includes invalid designer id.
        """

        url = "/games"
        data = {
            "title": "Civ VI",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 666, # designer id of 666 is invalid
            "categories": [ 1 ] 
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_game(self):
        """
        Test getting a single, valid, existing game from the DB.
        """
        self._seed_game_db()

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

    def test_get_nonexistent_single_game(self):
        """
        Test getting a game by an ID that is not in the database.
        """
        response = self.client.get('/games/666')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_games_on_empty_db(self):
        """
        Test getting all games when there are no games in the DB.
        """
        response = self.client.get('/games')
        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 0)

    def test_get_all_games(self):
        # seed db with three games
        self._seed_game_db(3)

        response = self.client.get('/games')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)

        self.assertEqual(json_response[0]["title"], "Civ VI")
        self.assertEqual(json_response[1]["title"], "NHL 20")
        self.assertEqual(json_response[2]["title"], "Persona V")

    def test_get_all_games_by_search_term(self):
        # seed db with three games
        self._seed_game_db(3)

        # search for persona -> should return Persona V
        response = self.client.get('/games?q=persona')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]["title"], "Persona V")

        # search for fun -> should return Civ VI and Persona V (matching on description text)
        response = self.client.get('/games?q=fun')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["title"], "Civ VI")
        self.assertEqual(json_response[1]["title"], "Persona V")

        # search for Firaxis -> should return all three games (matching on designer name)
        response = self.client.get('/games?q=Firaxis')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)
        self.assertEqual(json_response[0]["title"], "Civ VI")
        self.assertEqual(json_response[1]["title"], "NHL 20")
        self.assertEqual(json_response[2]["title"], "Persona V")

    def test_get_games_sorted_by_year(self):
        # seed db with three games
        self._seed_game_db(3)

        # get games ordered by year ascending
        response = self.client.get('/games?orderby=year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)
        self.assertEqual(json_response[0]["id"], 1)
        self.assertEqual(json_response[1]["id"], 3)
        self.assertEqual(json_response[2]["id"], 2)

        # get games ordered by year descending
        response = self.client.get('/games?orderby=year&direction=desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)
        self.assertEqual(json_response[0]["id"], 2)
        self.assertEqual(json_response[1]["id"], 3)
        self.assertEqual(json_response[2]["id"], 1)

    def test_get_games_sorted_by_duration(self):
        # seed db with three games
        self._seed_game_db(3)

        # get games ordered by duration ascending
        response = self.client.get('/games?orderby=duration')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)
        self.assertEqual(json_response[0]["id"], 2)
        self.assertEqual(json_response[1]["id"], 1)
        self.assertEqual(json_response[2]["id"], 3)

        # get games ordered by duration descending
        response = self.client.get('/games?orderby=duration&direction=desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 3)
        self.assertEqual(json_response[0]["id"], 3)
        self.assertEqual(json_response[1]["id"], 1)
        self.assertEqual(json_response[2]["id"], 2)

    def test_get_games_sorted_by_year_and_filtered_by_search_term(self):
        # seed db with three games
        self._seed_game_db(3)

        #get games with "fun" in description, ordered by year
        response = self.client.get('/games?q=fun&orderby=year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["id"], 1)
        self.assertEqual(json_response[1]["id"], 3)

    def test_valid_update_game(self):
        # seed db with one game
        self._seed_game_db(1)

        game = Game.objects.get(pk=1)
        self.assertEqual(game.title, "Civ VI")

        update = {
            "title": "Civ V",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1, 
            "categories": [ 1 ] 
        }

        response = self.client.put('/games/1', update, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        game = Game.objects.get(pk=1)
        self.assertEqual(game.title, "Civ V")

    def test_update_game_with_missing_required_property(self):
        # seed db with one game
        self._seed_game_db(1)

        # update body does not include required "title" property
        update = {
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1, 
            "categories": [ 1 ] 
        }

        response = self.client.put('/games/1', update, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_game_with_invalid_category_id(self):
        """
        Test creating a game that includes invalid category ids in categories array
        """
        # seed db with one game
        self._seed_game_db(1)

        update = {
            "title": "Civ VI",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1,
            "categories": [ 1, 666 ] # category id of 666 is invalid
        }

        response = self.client.put("/games/1", update, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_game_with_invalid_designer_id(self):
        """
        Test creating a game that includes invalid designer id.
        """
        # seed db with one game
        self._seed_game_db(1)

        update = {
            "title": "Civ VI",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 666, # designer id of 666 is invalid
            "categories": [ 1 ]
        }

        response = self.client.put("/games/1", update, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_game(self):
        """
        Test updating a game with an ID that does not exist
        """

        update = {
            "title": "Civ V",
            "description": "This fun game",
            "year": 2016,
            "numPlayers": 12,
            "estimatedDuration": 300,
            "ageRecommendation": 13,
            "designerId": 1,
            "categories": [ 1 ]
        }

        response = self.client.put("/games/1", update, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def _seed_game_db(self, count=1):
        """
        Manually create game data and insert into DB via ORM.
        """
        games = [
            Game(
                title="Civ VI", description="This fun game", year=2016,
                num_players=12, estimated_duration=300, age_recommendation=13, designer_id=1
            ),            
            Game(
                title="NHL 20", description="A bad game", year=2019,
                num_players=4, estimated_duration=15, age_recommendation=13, designer_id=1
            ),
            Game(
                title="Persona V", description="A very fun game", year=2017,
                num_players=1, estimated_duration=3000, age_recommendation=18, designer_id=1
            )
        ]

        game_categories = [
            [ GameCategory(game_id=1, category_id=1) ],
            [ GameCategory(game_id=3, category_id=2) ],
            [ GameCategory(game_id=2, category_id=1), GameCategory(game_id=2, category_id=3) ]
        ]

        for idx in range(count):
            game = games[idx]
            game.save()

            game_category_list = game_categories[idx]
            for game_category in game_category_list:
                game_category.save()

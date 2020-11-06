"""Game database model module"""
from django.db import models
from statistics import StatisticsError, mean

class Game(models.Model):
    """Game database model"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    year = models.IntegerField()
    num_players = models.IntegerField()
    estimated_duration = models.IntegerField()
    age_recommendation = models.IntegerField()
    designer = models.ForeignKey('raterapp.Designer', on_delete=models.CASCADE)

    @property
    def average_rating(self):
        """Unmapped model property for average rating of game"""
        reviews = self.gamereview_set.all()

        try:
            return mean([ review.rating for review in reviews ])

        except StatisticsError:
            return None

    @property
    def images(self):
        return self.gameimage_set.all()

    @property
    def categories(self):
        game_categories = self.game_categories.all()
        return [ gc.category for gc in game_categories ]

"""GameReview database model module"""
from django.db import models
from . import Game, Player

class GameReview(models.Model):
    """GameReview database model"""
    rating = models.IntegerField()
    review = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

"""GameImage database model module"""
from django.db import models
from . import Player, Game

class GameImage(models.Model):
    """GameImage database model"""
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

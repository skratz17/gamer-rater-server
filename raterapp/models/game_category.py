"""GameCategory database model module"""
from django.db import models
from . import Game, Category

class GameCategory(models.Model):
    """GameCategory database model"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_category")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="game_category")

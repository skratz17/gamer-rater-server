"""GameCategory database model module"""
from django.db import models

class GameCategory(models.Model):
    """GameCategory database model"""
    game = models.ForeignKey('raterapp.Game', on_delete=models.CASCADE, related_name="game_category")
    category = models.ForeignKey('raterapp.Category', on_delete=models.CASCADE, related_name="game_category")

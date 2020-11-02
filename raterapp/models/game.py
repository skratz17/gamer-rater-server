"""Game database model module"""
from django.db import models
from . import Designer

class Game(models.Model):
    """Game database model"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    year = models.IntegerField()
    num_players = models.IntegerField()
    estimated_duration = models.IntegerField()
    age_recommendation = models.IntegerField()
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)

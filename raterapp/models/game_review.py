"""GameReview database model module"""
from django.db import models

class GameReview(models.Model):
    """GameReview database model"""
    rating = models.IntegerField()
    review = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    game = models.ForeignKey('raterapp.Game', on_delete=models.CASCADE)
    player = models.ForeignKey('raterapp.Player', on_delete=models.CASCADE)

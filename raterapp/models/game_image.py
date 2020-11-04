"""GameImage database model module"""
from django.db import models

class GameImage(models.Model):
    """GameImage database model"""
    image = models.ImageField(upload_to='game_images', height_field=None, width_field=None, max_length=None, null=True)
    game = models.ForeignKey('raterapp.Game', on_delete=models.CASCADE)
    player = models.ForeignKey('raterapp.Player', on_delete=models.CASCADE)

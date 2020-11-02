"""Designer database model module"""
from django.db import models

class Designer(models.Model):
    """Designer database model"""
    name = models.CharField(max_length=150)

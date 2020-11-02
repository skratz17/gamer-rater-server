"""Category database model module"""
from django.db import models

class Category(models.Model):
    """Category database model"""
    name = models.CharField(max_length=50)
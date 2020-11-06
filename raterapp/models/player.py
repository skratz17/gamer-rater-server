"""Player database model module"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Player(models.Model):
    """Player database model"""
    bio = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

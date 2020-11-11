"""Models for accounts"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class AwaitingData(models.Model):
    """class to store data awaiting validation"""

    guid = models.UUIDField(default=uuid.uuid4)
    type = models.CharField(max_length=20)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Assigning unique"""

        unique_together = ("guid", "type", "key")


class CustomUser(AbstractUser):
    """Make user's email unique"""

    email = models.EmailField(unique=True)

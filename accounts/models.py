"""Models for accounts"""
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    """Redefine user to make email unique"""

    email = models.EmailField(unique=True)

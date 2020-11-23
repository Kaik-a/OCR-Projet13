"""Library's classes"""
from datetime import datetime
from uuid import uuid4

from django.db import models

from accounts.models import CustomUser


class Platform(models.Model):
    """Platforms for games"""

    name: str = models.CharField(max_length=100, primary_key=True, unique=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        """Platform's representation"""
        return f"{self.name}"


class Game(models.Model):
    """Games"""

    id: uuid4 = models.UUIDField(default=uuid4, primary_key=True)
    name: str = models.CharField(max_length=100)
    deck: str = models.CharField(max_length=5000)
    image: str = models.CharField(max_length=1000)
    giantbomb_url: str = models.CharField(max_length=500)
    platform: str = models.ForeignKey(Platform, on_delete=models.CASCADE)
    release_date: datetime = models.DateTimeField()

    class Meta:
        """Assigning unique"""

        unique_together = ("name", "giantbomb_url")

    def __repr__(self):
        """Game's representation"""
        return f"{self.name} on {self.platform}"


class PossessedGame(models.Model):
    """Games possessed by user"""

    id: uuid4 = models.UUIDField(default=uuid4, primary_key=True)
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game: Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    acquisition_date: datetime = models.DateTimeField(default=datetime.now)

    class Meta:
        """Assigning unique"""

        unique_together = ("user", "game")

    def __repr__(self):
        """Possessed's game representation"""
        return f"{self.game.name} owned by {self.user.username}"


class WantedGame(models.Model):
    """Wanted games"""

    id: uuid4 = models.UUIDField(default=uuid4, primary_key=True)
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game: Game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        """Assigning unique"""

        unique_together = ("user", "game")

    def __repr__(self):
        """Wanted game's representation"""
        return f"{self.game.name} wanted by {self.user.username}"


class LenderedGame(models.Model):
    """Lendered games"""

    id: uuid4 = models.UUIDField(default=uuid4, primary_key=True)
    game: PossessedGame = models.ForeignKey(PossessedGame, on_delete=models.CASCADE)
    borrower: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    not_registered_borrower: str = models.CharField(max_length=100)
    lendered_date: datetime = models.DateTimeField(default=datetime.now)
    return_date: datetime = models.DateTimeField(null=True)

    def __repr__(self):
        """Lendered game's representation"""
        return f"{self.game} borrowed by {self.borrower.username}"

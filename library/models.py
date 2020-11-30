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


class OwnedGame(models.Model):
    """Games owned by user"""

    id: uuid4 = models.UUIDField(default=uuid4, primary_key=True)
    user: CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game: Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    acquisition_date: datetime = models.DateTimeField(default=datetime.now)

    class Meta:
        """Assigning unique"""

        unique_together = ("user", "game")

    def __str__(self):
        """owned's game representation"""
        return f"{self.game.name}"


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


class LendedGame(models.Model):
    """lended games"""

    id: uuid4 = models.UUIDField(default=uuid4, primary_key=True)
    owned_game: OwnedGame = models.ForeignKey(OwnedGame, on_delete=models.CASCADE)
    borrower: CustomUser = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True
    )
    not_registered_borrower: str = models.CharField(max_length=100, null=True)
    lended_date: datetime = models.DateTimeField(default=datetime.now)
    return_date: datetime = models.DateTimeField(null=True)
    returned: bool = models.BooleanField(default=False)

    def __repr__(self):
        """lended game's representation"""
        return f"{self.owned_game} borrowed by {self.borrower.username}"

    class Meta:
        """A game can't be borrowed twice"""

        unique_together = ("owned_game", "returned")

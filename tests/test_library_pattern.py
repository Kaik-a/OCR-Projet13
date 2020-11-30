"""Library test pattern"""
from datetime import datetime

from accounts.models import Friends
from library import models
from library.models import LendedGame, OwnedGame, WantedGame
from tests.test_pattern import TestPattern


class TestLibrary(TestPattern):
    """class to test library's app"""

    def setUp(self) -> None:
        super().setUp()

        self.platform = models.Platform(
            name="PS4",
        )
        self.platform.save()

        self.game = models.Game(
            name="Game",
            platform=self.platform,
            release_date=datetime(day=21, month=10, year=1991),
        )
        self.game.save()

        self.owned_game = OwnedGame(user=self.user, game=self.game)
        self.owned_game.save()

        self.friend = Friends(user=self.user, friend=self.user2)
        self.friend.save()

        self.wanted_game = WantedGame(user=self.user, game=self.game)
        self.wanted_game.save()

        self.lended_game = LendedGame(
            owned_game=self.owned_game,
            borrower=self.user2,
            not_registered_borrower=None,
        )
        self.lended_game.save()

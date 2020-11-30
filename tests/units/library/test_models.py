"""Library's model"""
from datetime import datetime

from django.db import DataError

from library import models
from tests.test_pattern import TestPattern


class TestViews(TestPattern):
    """Test library's view"""

    def test_Game(self):
        """test on game's model"""
        with self.assertRaises(DataError):
            models.Game(
                name="Name really really really really really really really really "
                "really really really really really really really toooooooooooooooo"
                "oooooooooooooooooooooooooooooooooooooooooooooooooooooooo long",
                platform=self.platform,
                release_date=datetime(day=21, month=10, year=1991),
            ).save()

    def test_Platform(self):
        """test on platfotm's model"""
        with self.assertRaises(DataError):
            models.Platform(
                name="Name really really really really really really really really "
                "really really really really really really really too long really "
                "really really really really really really toooooooooooooooo"
                "oooooooooooooooooooooooooooooooooooooooooooooooooooooooo long"
            ).save()

    def test_lendedGame(self):
        """test on platfotm's model"""
        with self.assertRaises(ValueError):
            models.LendedGame(
                owned_game=self.game,
                borrower=self.user,
                not_registered_borrower=None,
                lended_date=datetime.now(),
                return_date=None,
            )

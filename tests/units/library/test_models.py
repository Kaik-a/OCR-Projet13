"""Library's model"""
from datetime import datetime

from django.db import DataError, IntegrityError, transaction

from library import models
from tests.test_library_pattern import TestLibrary


class TestViews(TestLibrary):
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

    def test_LendedGame(self):
        """test on platfotm's model"""
        models.LendedGame.objects.all().delete()

        lended_game = models.LendedGame(
            owned_game=self.owned_game,
            borrower=self.user,
            not_registered_borrower=None,
            lended_date=datetime.now(),
            return_date=None,
        )

        lended_game.save()

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                # It's not possiblie to lend two times same game
                models.LendedGame(
                    owned_game=self.owned_game,
                    borrower=self.user,
                    not_registered_borrower=None,
                    lended_date=datetime.now(),
                    return_date=None,
                ).save()

        # returned is automatically triggerd while return_date is set
        lended_game.returned = True

        lended_game.save()

        # As game is returned you can lend it
        models.LendedGame(
            owned_game=self.owned_game,
            borrower=self.user,
            not_registered_borrower=None,
            lended_date=datetime.now(),
            return_date=None,
        ).save()

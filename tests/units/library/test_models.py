"""Library's model"""
from datetime import datetime

from library import models
from tests.test_pattern import TestPattern


class TestViews(TestPattern):
    """Test library's view"""

    def setUp(self) -> None:
        self.platform = models.Platform(
            name="PS4",
            constructor="Sony",
            release_date=datetime(day=15, month=11, year=2013),
        )

        self.platform.save()

    def test_Game(self):
        """test on game's model"""
        with self.assertRaises(ValueError):
            models.Game(
                name="Name really really really really really really really really "
                "really really really really really really really too long",
                platform=self.platform,
                relase_date=datetime(21, 10, 1991),
                score=4,
            )

    def test_Platform(self):
        """test on platfotm's model"""
        with self.assertRaises(ValueError):
            models.Platform(
                name="PS5", constructor="Sony", release_date=datetime(19, 11, 2020)
            )

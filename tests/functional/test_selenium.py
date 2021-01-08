"""Selenium based tests template"""
import subprocess
from datetime import datetime

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from accounts.models import CustomUser, Friends
from library import models
from library.models import LendedGame, OwnedGame, WantedGame


class SeleniumBasedTestCase(LiveServerTestCase):
    """Test based on Selenium."""

    def setUp(self) -> None:
        """Set up tets environment"""
        self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")

        self.caps = DesiredCapabilities().FIREFOX.copy()
        self.caps["marionette"] = True
        self.binary = (
            subprocess.run(
                ["which", "firefox"], stdout=subprocess.PIPE, check=False
            ).stdout.decode("utf8")[:-1]
            or "/Applications/Applications/Firefox.app/Contents/MacOS/firefox-bin"  # noqa: W503
        )

        self.user = CustomUser.objects.create_user(
            username="test1", password="test1@1234", email="test@test.com"
        )

        self.user2 = CustomUser.objects.create_user(
            username="test2", password="test2@1234", email="test2@test.com"
        )

        self.driver = webdriver.Firefox(
            capabilities=self.caps,
            firefox_binary=self.binary,
        )

        self.driver.implicitly_wait(10)

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

    def tearDown(self) -> None:
        """Method to call at teardown."""
        self.driver.close()

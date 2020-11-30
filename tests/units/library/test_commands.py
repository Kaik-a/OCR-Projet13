"""Tests on library's commands"""
from unittest.mock import patch

from django.test import TestCase

from library.commands.commands import find_games, get_platform, get_release_date

from . import GAME


class TestCommand(TestCase):
    """class to test commands"""

    def test_get_platform(self):
        """Test get_plaform method"""
        self.assertEqual(get_platform(GAME, "PlayStation 4").name, "PlayStation 4")
        self.assertEqual(get_platform(GAME, "PlayStation").name, "PlayStation")
        self.assertEqual(get_platform(GAME, "PS5").name, "PlayStation")

    def test_get_release_date(self):
        """Test get_release_date method"""

        self.assertEqual(get_release_date(GAME), "1997-01-31")

        GAME["original_release_date"] = None

        GAME["release_date"] = "1997-02-01"

        self.assertEqual(get_release_date(GAME), "1997-02-01")

        GAME["release_date"] = None

        GAME["expected_release_year"] = "1997"

        self.assertEqual(get_release_date(GAME), "1997-01-01")

        GAME["expected_release_year"] = None

        self.assertEqual(get_release_date(GAME), "1970-01-01")

    def test_find_games(self):
        """Test find_games method"""

        def patch_request(**kwargs):
            """Don't send data to requests"""
            return [GAME]

        with patch("scrapping.send_requests.send_request", patch_request):

            games = find_games(query="Final Fantasy", query_platform="PlayStation")

            self.assertEqual(games[0].name, "Final Fantasy VII")

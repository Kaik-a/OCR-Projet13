"""Tests on library's commands"""
from unittest.mock import patch

from library.commands.commands import find_games, get_platform, get_release_date

from ...test_library_pattern import TestLibrary
from . import GAME


class TestCommand(TestLibrary):
    """class to test commands"""

    def test_get_platform(self):
        """Test get_plaform method"""
        # PlayStation 4 is required and is in game's platforms
        self.assertEqual(get_platform(GAME, "PlayStation 4").name, "PlayStation 4")
        # PlayStation is required and is in game's platforms
        self.assertEqual(get_platform(GAME, "PlayStation").name, "PlayStation")
        # PS5 is required and is not in game's platforms
        self.assertEqual(get_platform(GAME, "PS5").name, "PlayStation")

    def test_get_release_date(self):
        """Test get_release_date method"""

        # Take game original_release_dater
        self.assertEqual(get_release_date(GAME), "1997-01-31")

        GAME["original_release_date"] = None

        # No original_release_date set, get_release_date should take release_date
        self.assertEqual(get_release_date(GAME), "1997-02-01")

        GAME["release_date"] = None

        # No original_release_date nor release_date set, it should take
        # expected_release_year
        self.assertEqual(get_release_date(GAME), "1997-01-01")

        GAME["expected_release_year"] = None

        # No date are set, get_release_date should give a generic one
        self.assertEqual(get_release_date(GAME), "1970-01-01")

    def test_find_games(self):
        """Test find_games method"""

        def patch_request(**kwargs):
            """Don't send data to requests"""
            return [GAME]

        with patch("scrapping.send_requests.send_request", patch_request):

            games = find_games(query="Final Fantasy", query_platform="PlayStation")

            self.assertEqual(games[0].name, "Final Fantasy VII")

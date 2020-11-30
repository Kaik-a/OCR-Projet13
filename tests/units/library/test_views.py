"""Test library's views"""
from django.urls import reverse

from tests.test_library_pattern import TestLibrary


class TestViews(TestLibrary):
    """class to test library's view"""

    # path("your-games/<user>", views.your_games, name="your-games"),

    def setUp(self) -> None:
        super().setUp()
        self.HTTP_REFERER = "http://127.0.0.1/library/games/" + str(self.user.id)

    def test_add_to_library(self):
        """Load add_to_library"""
        url = reverse("library:add-to-library", kwargs={"game_": self.game.id})

        response = self.client.get(url, HTTP_REFERER=self.HTTP_REFERER)

        self.assertEqual(response.status_code, 302)

    def test_add_wish(self):
        """Load add wish"""
        url = reverse("library:add-wish", kwargs={"game_": self.game.id})

        response = self.client.get(url, HTTP_REFERER=self.HTTP_REFERER)

        self.assertEqual(response.status_code, 302)

    def test_borrowed(self):
        """Load borrowed"""
        url = reverse("library:borrowed")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_delete_from_library(self):
        """Load delete_from_library"""
        url = reverse(
            "library:delete-from-library",
            kwargs={"owned_game": self.owned_game.game.id},
        )

        response = self.client.get(url, HTTP_REFERER=self.HTTP_REFERER)

        self.assertEqual(response.status_code, 302)

    def test_delete_wish(self):
        """Load delete wish"""
        url = reverse(
            "library:delete-wish", kwargs={"wanted_game": self.wanted_game.game.id}
        )

        response = self.client.get(url, HTTP_REFERER=self.HTTP_REFERER)

        self.assertEqual(response.status_code, 302)

    def test_game(self):
        """Load game"""
        url = reverse("library:game", kwargs={"game_id": self.game.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_lended(self):
        """Load lended"""
        url = reverse("library:lended", kwargs={"user": self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_results(self):
        """Load results"""
        url = reverse(
            "library:results",
            kwargs={"platform": "Playstation", "query": "Final Fantasy VII"},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_unmark_lended(self):
        """Load unmark_lended"""
        url = reverse(
            "library:unmark-lended", kwargs={"lended_game": self.lended_game.id}
        )

        response = self.client.get(url, HTTP_REFERER=self.HTTP_REFERER)

        self.assertEqual(response.status_code, 302)

    def test_wanted(self):
        """Load wanted"""
        url = reverse("library:wanted", kwargs={"user": self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_your_games(self):
        """Load your_games"""
        url = reverse("library:your-games", kwargs={"user": self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

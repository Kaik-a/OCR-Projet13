"""Test library's views"""
from django.urls import reverse

from tests.test_library_pattern import TestLibrary


class TestViews(TestLibrary):
    """class to test library's view"""

    # path("delete-wish/<wanted_game>", views.delete_wish, name="delete-wish"),
    # path("game/<game_id>", views.game, name="game"),
    # path("lended/<user>", views.lended, name="lended"),
    # path("mark-lended/<owned_game>", views.mark_lended, name="mark-lended"),
    # path("results/<platform>/<query>", views.results, name="results"),
    # path("unmark-lended/<lended_game>", views.unmark_lended, name="unmark-lended"),
    # path("wanted/<user>", views.wanted, name="wanted"),
    # path("your-games/<user>", views.your_games, name="your-games"),

    def setUp(self) -> None:
        super().setUp()
        self.HTTP_REFERER = f"http://127.0.0.1/library/games/" + str(self.user.id)

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
        url = reverse("library:delete-wish")

        response = self.client.get(url, HTTP_REFERER=self.HTTP_REFERER)

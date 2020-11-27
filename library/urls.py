"""Urls for accounts"""
from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("add-to-library/<game_>", views.add_to_library, name="add-to-library"),
    path("add-wish/<game_>", views.add_wish, name="add-wish"),
    path("borrowed/<user>", views.borrowed, name="borrowed"),
    path(
        "delete-from-library/<owned_game>",
        views.delete_from_library,
        name="delete-from-library",
    ),
    path("delete-wish/<wanted_game>", views.delete_wish, name="delete-wish"),
    path("game/<game_id>", views.game, name="game"),
    path("lended/<user>", views.lended, name="lended"),
    path("mark-lended/<owned_game>", views.mark_lended, name="mark-lended"),
    path("results/<platform>/<query>", views.results, name="results"),
    path("unmark-lended/<lended_game>", views.unmark_lended, name="unmark-lended"),
    path("wanted/<user>", views.wanted, name="wanted"),
    path("your-games/<user>", views.your_games, name="your-games"),
]

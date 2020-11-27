"""Urls for accounts"""
from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("borrowed/<user>", views.borrowed, name="borrowed"),
    path("game/<game_id>", views.game, name="game"),
    path("lends/<user>", views.lends, name="lends"),
    path("results/<platform>/<query>", views.results, name="results"),
    path("wanted/<user>", views.wanted, name="wanted"),
    path("your-games/<user>", views.your_games, name="your-games"),
    path("add-wish/<game>", views.add_wish, name="add-wish"),
    path("delete-wish/<wanted_game>", views.delete_wish, name="delete-wish"),
    path("add-library/<game>", views.add_to_library, name="add-library"),
    path(
        "delete-library/<owned_game>", views.delete_from_library, name="delete-library"
    ),
    path("mark-lended/<owned_game>", views.mark_lended, name="mark-lended"),
    path("unmark-lended/<lended_game>", views.unmark_lended, name="unmark-lended"),
]

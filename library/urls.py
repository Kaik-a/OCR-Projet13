"""Urls for accounts"""
from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("add-to-library/<game_>", views.add_to_library, name="add-to-library"),
    path("add-wish/<game_>", views.add_wish, name="add-wish"),
    path("borrowed/", views.BorrowedView.as_view(), name="borrowed"),
    path(
        "delete-from-library/<owned_game>",
        views.delete_from_library,
        name="delete-from-library",
    ),
    path("delete-wish/<wanted_game>", views.delete_wish, name="delete-wish"),
    path("game/<game_id>", views.game, name="game"),
    path("games", views.GameListView.as_view(), name="games"),
    path("results/<platform>/<query>", views.results, name="results"),
    path("unmark-lended/<lended_game>", views.unmark_lended, name="unmark-lended"),
    path("wanted/", views.WantedView.as_view(), name="wanted"),
]

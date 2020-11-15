"""Urls for accounts"""
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("borrowed/<user>", views.borrowed, name="borrowed"),
    path("game/<id>", views.game, name="game"),
    path("lends/<user>", views.lends, name="lends"),
    path("results", views.results, name="results"),
    path("wanted/<user>", views.wanted, name="wanted"),
]

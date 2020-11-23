"""Library's commands"""
from typing import List
from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from library.models import Game, Platform
from scrapping import send_requests


def find_games(query: str, query_platform: str) -> List[Game]:
    """
    Find games based on platform.

    :param query: name of the game
    :param query_platform: game's platfomr
    :rtype: List[Game]
    """
    games_json = send_requests.send_request(query=query)

    games = []
    for game in games_json:
        platforms = game.get("platforms")

        if platforms:
            for platform in platforms:

                if platform["name"] == query_platform:
                    platform_name = query_platform
                    break
            else:
                platform_name = platforms[0]["name"]
        else:
            continue

        try:
            game_platform = Platform.objects.get(name=platform_name)
        except ObjectDoesNotExist:
            game_platform = Platform(name=platform_name)
            game_platform.save()
            game_platform = Platform.objects.get(name=platform_name)

        name = game.get("name")
        giantbomb_url = game.get("site_detail_url")

        if release_date := game.get("original_release_date"):
            release_date = str(release_date)
        elif release_date := game.get("expected_release_year"):
            release_date = str(release_date) + "-01-01"
        elif release_date := game.get("release_date"):
            release_date = str(release_date)
        else:
            release_date = "1970-01-01"

        try:
            game_ = Game(
                id=uuid4(),
                name=name,
                deck=game.get("deck"),
                giantbomb_url=giantbomb_url,
                image=game.get("image")["small_url"],
                platform=game_platform,
                release_date=release_date,
            )

            game_.save()

            games.append(game_)
        except IntegrityError:
            game_ = Game.objects.get(name=name, giantbomb_url=giantbomb_url)
            games.append(game_)

    return games

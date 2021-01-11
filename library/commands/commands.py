"""Library's commands"""
from typing import Dict, List, Union
from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from library.models import Game, Platform
from scrapping import send_requests


def get_platform(game: Dict, query_platform: str) -> Union[Platform, None]:
    """
    Get platform for a given game.

    :param game: Dict representation of a game
    :param query_platform: game's platform
    :return:
    """
    platforms = game.get("platforms")

    if platforms:
        for platform in platforms:

            if platform["name"] == query_platform:
                platform_name = query_platform
                break
        else:
            platform_name = platforms[0]["name"]
    else:
        return

    try:
        game_platform = Platform.objects.get(name=platform_name)
    except ObjectDoesNotExist:
        game_platform = Platform(name=platform_name)
        game_platform.save()
        game_platform = Platform.objects.get(name=platform_name)

    return game_platform


def get_release_date(game: Dict) -> str:
    """
    Get release date for game if exists
    :param game: game's representation
    :return: release_date
    """
    if game.get("original_release_date"):
        release_date = str(game.get("original_release_date"))
    elif game.get("release_date"):
        release_date = str(game.get("release_date"))
    elif game.get("expected_release_year"):
        release_date = str(game.get("expected_release_year")) + "-01-01"
    else:
        release_date = "1970-01-01"

    return release_date


def find_games(query: str, query_platform: str) -> List[Game]:
    """
    Find games based on platform.

    :param query: name of the game
    :param query_platform: game's platfomr
    :rtype: List[Game]
    """
    games_json = send_requests.send_request(query=query)

    if games_json == ["API unavailable"]:
        return games_json

    games = []
    for game in games_json:
        game_platform: Platform = get_platform(game, query_platform)

        if not game_platform:
            continue

        name = game.get("name")
        giantbomb_url = game.get("site_detail_url")
        release_date: str = get_release_date(game)

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

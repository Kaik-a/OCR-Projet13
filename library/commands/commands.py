"""Library's commands"""
from typing import List

from django.core.exceptions import ObjectDoesNotExist

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
        platform_name = ""
        for platform in platforms:

            if platform["name"] == query_platform:
                platform_name = query_platform
                break
        else:
            platform_name = platforms[0]["name"]

        try:
            game_ = Game(
                name=game.get("name"),
                deck=game.get("deck"),
                giantbomb_url=game.get("site_detail_url"),
                image=game.get("image")["small_url"],
                platform=Platform.objects.get(name=platform_name),
                release_date=game.get("original_release_date")
                or game.get("expected_release_year"),
            )
            game_.save()

            games.append(game_)
        except ObjectDoesNotExist:
            continue
        except Exception as error:
            continue

    return games

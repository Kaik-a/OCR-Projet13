"""Library's commands"""
from typing import List

from library.models import Game
from scrapping import send_requests


def find_games(platform: str, query: str) -> List[Game]:
    """
    Find games based on platform.

    :param platform: game's platfomr
    :param query: name of the game
    :rtype: List[Game]
    """
    games_json = send_requests.send_request(query=query)

    games = []
    for game in games_json:
        try:
            games.append(
                Game(
                    name=game.get("name"),
                    description=game.get("deck"),
                    giantbomb_url=game.get("site_detail_url"),
                    image_url=game.get("image")["small_url"],
                    platform=game.get("platforms"),
                    release_date=game.get("expected_realease_year"),
                )
            )
        except:
            continue

    [game.save() for game in games]

    return games

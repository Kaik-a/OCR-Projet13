"""Get lended games"""
from typing import Union

from django import template
from django.core.exceptions import ObjectDoesNotExist

from library.models import LendedGame

register = template.Library()


@register.filter(name="get_lended")
def get_lended(owned_game_id) -> Union[LendedGame, bool]:
    """
    Get lended games.

    :param owned_game_id: id of game owned
    :rtype: Union[LendedGame, bool]
    """
    try:
        lended_game = LendedGame.objects.get(owned_game=owned_game_id, returned=False)
        return lended_game
    except ObjectDoesNotExist:
        return False

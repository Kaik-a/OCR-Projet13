"""Views for library"""
from django.http import HttpResponse


def borrowed(request, user: str) -> HttpResponse:
    """
    Display borrowed games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    return None


def game(request, game_id: int) -> HttpResponse:
    """
    Load game's page.

    :param request: Django's request
    :param game_id: Game's id
    :rtype: HttpResponse
    """
    return None


def lends(request, user: str) -> HttpResponse:
    """
    Didplay lended games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    return None


def results(request, query: str) -> HttpResponse:
    """
    Display results for a given query.

    :param request: Django's request
    :param query: query to look for
    :rtype: HttpResponse
    """
    return None


def wanted(request, user: str) -> HttpResponse:
    """
    Display wanted games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    return None

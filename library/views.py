"""Views for library"""
from typing import List, Union

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.models import CustomUser
from library.models import Game, LenderedGame, WantedGame
from scrapping.send_requests import send_request


def borrowed(request, user: str) -> HttpResponse:
    """
    Display borrowed games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    borrower: CustomUser = CustomUser.objects.get(id=user)
    try:
        borrowed_games: Union[
            List[LenderedGame], LenderedGame
        ] = LenderedGame.objects.filter(borrower=borrower)
    except:
        # TODO: message telling no games borrowed yet
        return render(request, "borrowed.html")

    context = {"borrowed_games": borrowed_games}

    return render(request, "borrowed.html", context)


def game(request, game_id: int) -> HttpResponse:
    """
    Load game's page.

    :param request: Django's request
    :param game_id: Game's id
    :rtype: HttpResponse
    """
    try:
        game_: Game = Game.objects.get(id=game_id)
    except:
        # TODO "this game isn't in our db"
        return render(request, "game.html")

    return render(request, "game.html", {"game": game_})


def lends(request, user: str) -> HttpResponse:
    """
    Didplay lended games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    lender: CustomUser = CustomUser.objects.get(id=user)

    try:
        lendered_games: Union[
            List[LenderedGame], LenderedGame
        ] = LenderedGame.objects.filter(lender=lender)
    except:
        # TODO: "no game lendered"
        return render(request, "lendered.html")

    return render(request, "lendered.html", {"lendered_games": lendered_games})


def results(request, query: str) -> HttpResponse:
    """
    Display results for a given query.

    :param request: Django's request
    :param query: query to look for
    :rtype: HttpResponse
    """
    try:
        game_list = send_request(query=query, resources="game")
    except:
        return redirect(reverse("home"))

    return render(request, "library:results", {"games": game_list})


def wanted(request, user: str) -> HttpResponse:
    """
    Display wanted games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    user_ = CustomUser.objects.get(id=user)

    try:
        wanted_games: Union[List[WantedGame], WantedGame] = WantedGame.objects.filter(
            user=user_
        )
    except:
        return redirect(reverse("home"))

    return render(request, "wanted.html", {"wanted_games": wanted_games})

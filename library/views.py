"""Views for library"""
from datetime import datetime
from typing import List, Union

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.models import CustomUser, Friends
from library.forms import LendGameForm, SearchGameForm
from library.models import Game, LendedGame, OwnedGame, WantedGame

from .commands.commands import find_games


def borrowed(request) -> HttpResponse:
    """
    Display borrowed games for a given user.

    :param request: Django's request
    :rtype: HttpResponse
    """
    try:
        borrowed_games = LendedGame.objects.filter(borrower=request.user)
    except ObjectDoesNotExist:
        messages.add_message(request, 25, "Vous n'avez pas encore emprunté de jeu")
        return render(request, "borrowed.html")

    borrowed_games = [borrowed_game.owned_game.game for borrowed_game in borrowed_games]
    context = {"games": borrowed_games}

    return render(request, "borrowed.html", context)


def game(request, game_id: str) -> HttpResponse:
    """
    Load game's page.

    :param request: Django's request
    :param game_id: Game's id
    :rtype: HttpResponse
    """
    try:
        game_: Game = Game.objects.get(id=game_id)
    except ObjectDoesNotExist:
        return render(request, "games.html")

    return render(request, "game.html", {"game": game_})


def lended(request, user: str) -> HttpResponse:
    """
    Display lended games for a given user.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    lender: CustomUser = CustomUser.objects.get(id=user)

    if request.method == "POST":
        form: LendGameForm = LendGameForm(request.POST, user=request.user)

        if form.is_valid():
            owned_game = OwnedGame.objects.get(id=form.data.get("owned_game"))

            borrower = form.data.get("borrower")

            if borrower:
                borrower = Friends.objects.get(id=borrower).friend
            unknown_borrower = form.data.get("unknown_borrower")

            try:
                lended_game = LendedGame(
                    owned_game=owned_game,
                    borrower=borrower if borrower else None,
                    not_registered_borrower=unknown_borrower,
                    lended_date=datetime.now(),
                    return_date=None,
                )
                lended_game.save()

                messages.add_message(
                    request,
                    25,
                    f"Le jeu {owned_game.game.name} a été enregistré comme prêté "
                    f"à {borrower.username if borrower else unknown_borrower}",
                )
            except IntegrityError:
                messages.add_message(
                    request,
                    40,
                    "Le jeu que vous souhaitez ajouter a déjà été emprunté",
                )

    else:
        form: LendGameForm = LendGameForm(user=request.user)

    try:
        lended_games: Union[List[LendedGame], LendedGame] = LendedGame.objects.filter(
            owned_game__user=lender
        )
    except ObjectDoesNotExist:
        messages.add_message(request, 25, "Vous n'avez prêté aucun jeu")
        return render(request, "lended.html")

    return render(request, "lended.html", {"form": form, "games": lended_games})


def results(request, platform: str, query: str) -> HttpResponse:
    """
    Display results for a given query.

    :param request: Django's request
    :param platform: game's platform
    :param query: query to look for
    :rtype: HttpResponse
    """
    game_list = find_games(query=query, query_platform=platform)

    return render(request, "results.html", {"games": game_list})


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
    except ObjectDoesNotExist:
        messages.add_message(
            request, 25, "Vous n'avez aucun jeu dans votre liste d'envies"
        )
        return redirect(reverse("home"))

    games = [wanted_game.game for wanted_game in wanted_games]

    return render(request, "wanted.html", {"games": games})


def your_games(request, user: str) -> HttpResponse:
    """
    Display user's games.

    :param request: Django's request
    :param user: gamelender user
    :rtype: HttpResponse
    """
    user_: CustomUser = CustomUser.objects.get(id=user)

    games: Union[List[OwnedGame], OwnedGame] = OwnedGame.objects.filter(user=user_)
    if request.method == "POST":
        form: SearchGameForm = SearchGameForm(request.POST)

        if form.is_valid():
            return redirect(
                reverse(
                    "library:results",
                    kwargs={
                        "platform": form.data.get("platform"),
                        "query": form.data.get("game"),
                    },
                )
            )
    else:
        form: SearchGameForm = SearchGameForm()

    games: Union[List[Game], Game] = [owned_game.game for owned_game in games]

    return render(request, "games.html", {"form": form, "games": games})


def add_wish(request, game_: str) -> HttpResponseRedirect:
    """
    Add a game to user's wish list.

    :param request: django's request
    :param game_: game to add to wish list
    :rtype: HttpResponseRedirect
    """
    game_: Game = Game.objects.get(id=game_)
    wanted_game: WantedGame = WantedGame(user=request.user, game=game_)
    try:
        wanted_game.save()

        messages.add_message(
            request,
            25,
            f"Le jeu {game_.name} a été correctement ajouté à votre liste d'envies",
        )
    except IntegrityError as error:
        messages.add_message(
            request,
            40,
            f"Une erreur a été rencontré lors de l'ajout du jeu {wanted_game.game.name}"
            f" à votre liste d'envies: {error}",
        )

    return HttpResponseRedirect(request.environ["HTTP_REFERER"])


def delete_wish(request, wanted_game: WantedGame) -> HttpResponseRedirect:
    """
    Delete a game which was in wish list.

    :param request: django's request
    :param wanted_game: game to delete from wish list
    :rtype: HttpResponseRedirect
    """
    wanted_game: WantedGame = WantedGame.objects.get(
        user=request.user, game=Game.objects.get(id=wanted_game)
    )

    try:
        wanted_game.delete()

        messages.add_message(
            request,
            25,
            f"Le jeu {wanted_game.game.name} a été correctement supprimé de votre "
            f"liste d'envies",
        )
    except IntegrityError as error:
        messages.add_message(
            request,
            40,
            f"Une erreur a été rencontrée lors de la suppression du jeu "
            f"{wanted_game.game.name}: {error}",
        )

    return HttpResponseRedirect(request.environ["HTTP_REFERER"])


def add_to_library(request, game_: str) -> HttpResponseRedirect:
    """
    Add a game to user's library.

    :param request: django's request
    :param game_: game to add to library
    :rtype: HttpResponseRedirect
    """
    game_: Game = Game.objects.get(id=game_)
    new_game: OwnedGame = OwnedGame(user=request.user, game=game_)

    try:
        new_game.save()

        messages.add_message(
            request,
            25,
            f"Le jeu {game_.name} a été correctement ajouté à votre bibliothèque",
        )
    except IntegrityError:
        messages.add_message(
            request,
            40,
            f"Le jeu {game_.name} fait déjà partie de votre bibliothèque",
        )

    return HttpResponseRedirect(request.environ["HTTP_REFERER"])


def delete_from_library(request, owned_game: OwnedGame) -> HttpResponseRedirect:
    """
    Delete a game from user's library.

    :param request: django's request
    :param owned_game: game to delete from the library
    :rtype: HttpResponseRedirect
    """
    try:
        owned_game: OwnedGame = OwnedGame.objects.get(
            user=request.user, game__id=owned_game
        )

        owned_game.delete()

        messages.add_message(
            request,
            25,
            f"Le jeu {owned_game.game.name} a été correctement supprimé de votre "
            f"bibliothèque",
        )
    except IntegrityError as error:
        messages.add_message(
            request,
            40,
            f"Une erreur a été rencontrée lors de la suppression du jeu "
            f"{owned_game.game.name}: {error}",
        )

    return HttpResponseRedirect(request.environ["HTTP_REFERER"])


def unmark_lended(request, lended_game: LendedGame) -> HttpResponseRedirect:
    """
    Unmark a game which has been lended.

    :param request: django's request
    :param lended_game: game lended
    :rtype: HttpResponseRedirect
    """
    lended_game_ = LendedGame.objects.get(id=lended_game)
    try:
        lended_game_.return_date = datetime.now()
        lended_game_.returned = True

        lended_game_.save()

        borrower = lended_game_.borrower
        messages.add_message(
            request,
            25,
            f"Le jeu {lended_game_.owned_game.game.name} emprunté par "
            f"{borrower.username if borrower else lended_game_.not_registered_borrower}"
            f"a été correctement supprimé de vos jeux empruntés",
        )
    except IntegrityError as error:
        messages.add_message(
            request,
            40,
            f"Une erreur a été rencontrée lors de la suppression du jeu "
            f"{lended_game_.owned_game.game.name}: {error}",
        )

    return HttpResponseRedirect(request.environ["HTTP_REFERER"])

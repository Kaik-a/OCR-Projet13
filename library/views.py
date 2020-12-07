"""Views for library"""
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView

from accounts.models import Friends
from library.forms import LendGameForm
from library.models import Game, LendedGame, OwnedGame, WantedGame

from .commands.commands import find_games
from .context_processors.navbar_search_decorator import navbar_search_decorator


@method_decorator(navbar_search_decorator, name="dispatch")
class BorrowedView(ListView, LoginRequiredMixin):
    """Load borrowed games"""

    model = LendedGame

    template_name = "borrowed.html"
    context_object_name = "borrowed_games"
    paginate_by = 10

    def get_queryset(self):
        """Get borrowed games"""
        return self.model.objects.filter(borrower=self.request.user)

    def get_context_data(self, **kwargs):
        """Construct context"""
        context = super().get_context_data(**kwargs)
        borrowed_games = self.get_queryset()
        page = self.request.GET.get("page")
        paginator = Paginator(borrowed_games, self.paginate_by)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        context["games"] = games
        return context


@login_required
@navbar_search_decorator
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
        return render(request, "game_view.html")

    return render(request, "game.html", {"game": game_})


@login_required
@navbar_search_decorator
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


@method_decorator(navbar_search_decorator, name="dispatch")
class WantedView(ListView, LoginRequiredMixin):
    """Load wanted games"""

    model = WantedGame
    template_name = "wanted.html"
    context_object_name = "wanted_games"
    paginate_by = 10

    def get_queryset(self):
        """Get wanted games"""
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Construct context"""
        context = super().get_context_data(**kwargs)
        wanted_games = self.get_queryset()
        page = self.request.GET.get("page")
        paginator = Paginator(wanted_games, self.paginate_by)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        context["games"] = games
        return context


@method_decorator(navbar_search_decorator, name="dispatch")
class GameListView(ListView, FormView, LoginRequiredMixin):
    """Load owned games"""

    model = OwnedGame
    template_name = "game_view.html"
    context_object_name = "owned_games"
    paginate_by = 10

    form_class = LendGameForm
    success_url = "games"

    def get_form_kwargs(self):
        """Get user in form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Action if form is valid"""
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
                self.request,
                25,
                f"Le jeu {owned_game.game.name} a été enregistré comme prêté "
                f"à {borrower.username if borrower else unknown_borrower}",
            )
        except IntegrityError:
            messages.add_message(
                self.request,
                40,
                "Le jeu que vous souhaitez ajouter a déjà été emprunté",
            )
        return super().form_valid(form)

    def get_queryset(self):
        """Get owned games"""
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Construct context"""
        context = super().get_context_data(**kwargs)
        owned_games = self.get_queryset()
        page = self.request.GET.get("page")
        paginator = Paginator(owned_games, self.paginate_by)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        context["games"] = games
        return context


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def unmark_lended(request, lended_game: LendedGame) -> HttpResponseRedirect:
    """
    Unmark a game which has been lended.

    :param request: django's request
    :param lended_game: game lended
    :rtype: HttpResponseRedirect
    """
    lended_game_ = LendedGame.objects.get(id=lended_game)
    try:
        lended_game_.returned = True

        lended_game_.save()

        borrower = lended_game_.borrower
        messages.add_message(
            request,
            25,
            f"Le jeu {lended_game_.owned_game.game.name} emprunté par "
            f"{borrower.username if borrower else lended_game_.not_registered_borrower}"
            f" a été correctement supprimé de vos jeux empruntés",
        )
    except IntegrityError as error:
        messages.add_message(
            request,
            40,
            f"Une erreur a été rencontrée lors de la suppression du jeu "
            f"{lended_game_.owned_game.game.name}: {error}",
        )

    return HttpResponseRedirect(request.environ["HTTP_REFERER"])

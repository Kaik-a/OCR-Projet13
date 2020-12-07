"""Views for accounts"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView

from library.context_processors.navbar_search_decorator import navbar_search_decorator

from .commands.commands import mail_password, mail_subscription, validate_subscription
from .forms import (
    ChangePasswordForm,
    CheckMailForm,
    LoginForm,
    SearchFriendForm,
    SubscribeForm,
)
from .models import AwaitingData, CustomUser, Friends


def login_user(request, form: LoginForm) -> HttpResponse:
    """
    Verify login.

    :param request: django request
    :param LoginForm form: form to retrieve login data
    :return: HttpResponse
    """
    # Get credentials
    username = form.data.get("login")
    password = form.data.get("password")

    if username and password:
        # Authenticate with given credentials
        user: CustomUser = authenticate(
            username=username,
            password=password,
        )
        # A user exists with given credentials
        if user:
            login(request, user)
            messages.add_message(
                request, 25, f"Bonjour {user.first_name}! Vous êtes maintenant connecté"
            )
            return redirect(reverse("accounts:user_account"))

        # No user found
        messages.add_message(
            request,
            40,
            "Aucun compte recensé avec cette combinaison. Votre email ou mot de "
            "passe sont peut être incorrects?",
        )
        return render(request, "login.html", {"form": form})

    return render(request, "login.html", {"form": form})


def get_user_info(request) -> HttpResponse:
    """
    View to send login data.

    :param request: django request
    :return: HttpResponse
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            return login_user(request, form)
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def subscribe(request) -> HttpResponse:
    """
    View to subscribe for a new user.

    :param request: django request
    :return: HttpResponse
    """
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            try:
                mail_subscription(request, form.data)

                return redirect("accounts:login")
            except IntegrityError as error:
                messages.add_message(
                    request, 40, f"Echec lors de la création du compte: {error}"
                )
            form_connect = LoginForm()

            return redirect(reverse("accounts:login"), form=form_connect)
    else:
        form = SubscribeForm()

    return render(request, "subscribe.html", {"form": form})


def validate(request, guid: str) -> HttpResponse:
    """
    Validate data through a link received by mail.

    :param request: django's request
    :param guid: Guid to identify request sent
    :return: HttpResponse
    """
    try:
        to_validate = AwaitingData.objects.filter(guid=guid)

        type_of_validation = to_validate[0].type
        if type_of_validation == "subscription":
            validate_subscription(request, guid)

            to_validate.delete()
            return redirect(reverse("home"))

        user = CustomUser.objects.get(id=to_validate[0].value).id
        if user:
            to_validate.delete()

        return redirect(reverse("accounts:reset_password", args=[user]))

    except Exception:  # pylint: disable=W0703
        messages.add_message(
            request,
            40,
            "Le lien utilisé n'est plus actif, veuillez refaire la procédure.",
        )

    return redirect(reverse("home"))


def send_reset(request, user: str) -> HttpResponse:  # pylint: disable=W0613
    """
    Send email to user to change password.

    :param request: django's request
    :param str user: user to change password
    :return:
    """
    mail_password(request, user)

    return redirect(reverse("home"))


def reset_password(request, user: str) -> HttpResponse:
    """
    Reset user's password.

    :param request: django's request
    :param str user: user to change password
    :return: HttpResponse
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            user = CustomUser.objects.get(id=user)
            if user:
                user.set_password(form.data.get("new_password"))

                user.save()

                messages.add_message(
                    request, 25, "Votre mot de passe à correctement été mis à jour"
                )
                return redirect(reverse("accounts:login"), user=user)
    else:
        form = ChangePasswordForm()

    return render(request, "reset_password.html", {"form": form})


def check_mail(request) -> HttpResponse:
    """
    Check if mail is integration database.

    :param request: django's request
    :return: HttpResponse
    """
    if request.method == "POST":
        form = CheckMailForm(request.POST)

        if form.is_valid():
            email = form.data.get("email")
            try:
                user = CustomUser.objects.get(email=email).id

                if user:
                    messages.add_message(
                        request,
                        25,
                        f"Un mail vous a été envoyé à l'adresse {email} "
                        f"pour changer votre mot de passe",
                    )
                    return redirect(reverse("accounts:send_reset", args=[user]))

                messages.add_message(
                    request,
                    40,
                    f"Aucun compte n'a été trouvé avec l'adresse {email}",
                )
                return render(request, "check_mail.html", {"form": form})
            except Exception as error:  # pylint: disable=W0703
                messages.add_message(
                    request,
                    40,
                    f"{error}\nNous ne retrouvons pas d'utilisateur avec le mail {email}",
                )
    else:
        form = CheckMailForm()

    return render(request, "check_mail.html", {"form": form})


@login_required
def sign_out(request) -> HttpResponse:
    """
    View to log out.

    :param request: django request
    :return: HttpResponse
    """
    logout(request)

    messages.add_message(request, 25, "Au revoir!")
    return redirect(reverse("home"))


@login_required
@navbar_search_decorator
def user_account(request) -> HttpResponse:
    """
    View to get user accounts.

    :param request: django request
    :return: HttpResponse
    """
    return render(request, "user_account.html")


@method_decorator(navbar_search_decorator, name="dispatch")
class FriendsView(ListView, FormView, LoginRequiredMixin):
    """Load friends page"""

    model = Friends
    template_name = "friends.html"
    context_object_name = "friends"
    paginate_by = 10

    form_class = SearchFriendForm
    success_url = "friends"

    def get_form_kwargs(self):
        """Add user to form's kwargs"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Action after form's validation"""
        user = self.request.user
        try:
            friend_to_add: CustomUser = CustomUser.objects.get(id=form.data.get("user"))

            relationship = Friends(user=user, friend=friend_to_add)

            relationship.save()

            messages.add_message(
                self.request,
                25,
                f"L'utilisateur {friend_to_add.username} a été ajouté à vos amis",
            )
        except ObjectDoesNotExist:
            messages.add_message(
                self.request,
                40,
                f"Aucun utilisateur trouvé ayant pour nom d'utilisateur {friend_to_add.username}",
            )
        except IntegrityError:
            messages.add_message(
                self.request, 40, f"Vous êtes déjà ami avec {friend_to_add.username}"
            )

        return super().form_valid(form)

    def get_queryset(self):
        """Get Friends in db"""
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Construct context for template"""
        context = super().get_context_data(**kwargs)
        relations = self.get_queryset()
        page = self.request.GET.get("page")
        paginator = Paginator(relations, self.paginate_by)
        try:
            friends_ = paginator.page(page)
        except PageNotAnInteger:
            friends_ = paginator.page(1)
        except EmptyPage:
            friends_ = paginator.page(paginator.num_pages)
        context["friends"] = friends_
        return context


def delete_friend(request, friend: CustomUser) -> HttpResponse:
    """
    Delete a friend from friend's list

    :param request: django's request
    :param friend: friend to delete
    :rtype: HttpResponse
    """
    try:
        Friends.objects.get(
            user=request.user.id, friend=CustomUser.objects.get(username=friend)
        ).delete()

        messages.add_message(
            request, 25, f"L'utilisateur {friend} a bien été supprimé de vos amis"
        )
    except IntegrityError:
        pass

    return redirect(reverse("accounts:friends"))

"""Commands for accounts"""
import uuid
from typing import Dict

from django.contrib import messages
from django.core.mail import send_mail

from accounts.models import AwaitingData, CustomUser


def validate_subscription(request, guid: str) -> None:
    """
    Create account after validation.

    :param request: django's request
    :param guid: Subscription guid
    :rtype: None
    """
    try:
        CustomUser.objects.create_user(
            username=AwaitingData.objects.get(guid=guid, key="login").value,
            password=AwaitingData.objects.get(guid=guid, key="password").value,
            first_name=AwaitingData.objects.get(guid=guid, key="first_name").value,
            last_name=AwaitingData.objects.get(guid=guid, key="last_name").value,
            email=AwaitingData.objects.get(guid=guid, key="email").value,
        )

        messages.add_message(
            request,
            25,
            f"L'utilisateur "
            f"{AwaitingData.objects.get(guid=guid, key='login').value}"
            f" a bien été créé, vous pouvez dès à présent vous connecter",
        )

    except Exception as error:  # pylint: disable=W0703
        messages.add_message(
            request,
            40,
            f"Echec lors de la création du compte: {error}, "
            f"si le problème se reproduit, veuillez contacter"
            f" le support",
        )


def mail_subscription(request, data: Dict) -> None:
    """
    Send mail for subscription.

    :param request: django's request
    :param Dict data: data sent integration subscription
    :rtype: None
    """
    guid = uuid.uuid4()

    for key, value in data.items():
        if key == "csrfmiddlewaretoken":
            continue
        AwaitingData(guid=guid, type="subscription", key=key, value=value).save()

    subject = "Création de compte"
    message = (
        f'Bonjour {data.get("first_name")},\n'
        f"\n"
        f"Vous venez de créer un compte sur Pur Beurre et nous "
        f"vous en remercions.\n"
        f"\n"
        f"Afin de valider votre souscription, merci de cliquer sur"
        f" le lien suivant. \n"
        f"\n"
        f"http://127.0.0.1:8000/accounts/validate/{guid}\n"
        f"\n"
        f"Ce lien sera valide 24h.\n"
        f"\n"
        f"Cordialement,\n"
        f"\n"
        f"L'équipe Pur Beurre"
    )

    send_mail(subject, message, "pur.beurre.mbi@gmail.com", [data.get("email")])

    messages.add_message(
        request,
        25,
        f"Un email vous a été envoyé à l'adresse {data.get('email')} "
        f"veuillez utiliser le lien fourni afin de valider votre compte",
    )


def mail_password(user: str):
    """
    Send mail to reset password.

    :param str user: user to reset password
    """
    user = CustomUser.objects.get(id=user)
    guid = uuid.uuid4()
    AwaitingData(guid=guid, type="password", key="user", value=user.id).save()

    subject = "Changement de mot de passe"
    message = (
        f"Bonjour {user.first_name},\n"
        f"\n"
        f"Vous avez oublié votre mot de passe ?\n"
        f"\n"
        f"Veuillez suivre le lien suivant pour le changer\n"
        f"\n"
        f"http://127.0.0.1:8000/accounts/validate/{guid}\n"
        f"\n"
        f"Ce lien sera valide 24h.\n"
        f"\n"
        f"Cordialement,\n"
        f"\n"
        f"L'équipe Pur Beurre"
    )
    send_mail(subject, message, "pur.beurre.mbi@gmail.com", [user.email])

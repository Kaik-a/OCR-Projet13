"""Forms for accounts"""
from typing import Dict

from django import forms

from accounts.models import CustomUser, Friends


class LoginForm(forms.Form):
    """Class to create form for user."""

    login = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SubscribeForm(forms.Form):
    """Class to create form for creating user."""

    login = forms.CharField(label="Login", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=120)
    first_name = forms.CharField(label="Prénom", max_length=50)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmer", widget=forms.PasswordInput)

    def clean(self):
        """Get cleaned data"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas")


class CheckMailForm(forms.Form):
    """Class to create form to check is email integration db"""

    email = forms.EmailField(label="E-mail")


class ChangePasswordForm(forms.Form):
    """Class to create form integration order to change password"""

    new_password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(
        label="Confirmer", widget=forms.PasswordInput
    )

    def clean(self):
        """Get cleaned data"""
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas")


class SearchFriendForm(forms.Form):
    """Class to create form in order to look for a friend"""

    user = None

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)
        self.fields["user"] = forms.ModelChoiceField(
            label="",
            empty_label="",
            queryset=CustomUser.objects.exclude(username=user)
            .filter(
                is_superuser=False,
                is_active=True,
            )
            .exclude(user_friend__in=Friends.objects.filter(user=user)),
        )
        form_id: Dict = {"id": "search-friend-form"}
        self.fields["user"].widget.attrs.update(form_id)

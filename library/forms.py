"""Forms for library"""
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Friends
from library.models import OwnedGame, Platform


class SearchGameForm(forms.Form):
    """Class to create form for user."""

    game = forms.CharField(label="Nom du jeu")
    platform = forms.ModelChoiceField(
        label="Plateforme",
        empty_label="",
        queryset=Platform.objects.order_by("name"),
        to_field_name="name",
    )


class LendGameForm(forms.Form):
    """class to create lending game form"""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["owned_game"] = forms.ModelChoiceField(
            label="Jeu",
            empty_label="",
            queryset=OwnedGame.objects.filter(user=user),
        )
        self.fields["borrower"] = forms.ModelChoiceField(
            label="Ami",
            empty_label="",
            queryset=Friends.objects.filter(user=user),
            required=False,
        )
        self.fields["unknown_borrower"] = forms.CharField(
            label="Emprunteur", max_length=100, required=False
        )

    game = None
    borrower = None
    unknown_borrower = None

    def clean(self):
        """Make sure either borrower or unknown_borrower are filled"""
        cleaned_data = super().clean()

        borrower = cleaned_data.get("borrower")
        unknown_borrower = cleaned_data.get("unknown_borrower")

        if not borrower and not unknown_borrower:
            raise ValidationError(
                "Either borrrower or unknown_borrowed should be filled"
            )
        return cleaned_data

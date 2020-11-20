"""Forms for library"""
from django import forms

from library.models import Platform


class SearchGameForm(forms.Form):
    """Class to create form for user."""

    game = forms.CharField(label="Nom du jeu")
    platform = forms.ModelChoiceField(
        label="Plateforme",
        empty_label="",
        queryset=Platform.objects.order_by("name"),
        to_field_name="name",
    )

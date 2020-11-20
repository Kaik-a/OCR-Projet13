"""Forms for library"""
from django import forms

from library.models import Platform


class SearchGameForm(forms.Form):
    """Class to create form for user."""

    game = forms.CharField(label="Nom du jeu")
    platform = forms.ModelChoiceField(
        label="Plateforme", queryset=Platform.objects.all()
    )

"""Test library's forms"""
from library.forms import LendGameForm, SearchGameForm
from tests.test_library_pattern import TestLibrary


class TestForms(TestLibrary):
    """Class to test forms"""

    def test_search_game_form(self):
        """Test SearchGameForm"""
        # PS4 is in database so form should be valid
        form = SearchGameForm(data={"game": "Final Fantasy VII", "platform": "PS4"})

        self.assertTrue(form.is_valid())

        # As PS2 is not in database, form shouldn't be valid
        form = SearchGameForm(data={"game": "Final Fantasy VII", "platform": "PS2"})

        self.assertFalse(form.is_valid())

    def test_lend_game_form(self):
        """Test LendGameForm"""
        form = LendGameForm(
            user=self.user,
            data={
                "owned_game": self.owned_game,
                "borrower": self.friend,
                "unknown_borrower": None,
            },
        )

        # Form filled with no unknown borrower should be valid
        self.assertTrue(form.is_valid())

        # Form filled with no borrower should be valid
        form = LendGameForm(
            user=self.user,
            data={
                "owned_game": self.owned_game,
                "borrower": None,
                "unknown_borrower": "Mike",
            },
        )

        self.assertTrue(form.is_valid())

        # Form with no borrower nor unknown_borrower should not be valid
        form = LendGameForm(
            user=self.user,
            data={
                "owned_game": self.owned_game,
                "borrower": None,
                "unknown_borrower": None,
            },
        )
        self.assertFalse(form.is_valid())

    # class LendGameForm(forms.Form):
    #     """class to create lending game form"""
    #
    #     def __init__(self, *args, **kwargs):
    #         user = kwargs.pop("user", None)
    #         super().__init__(*args, **kwargs)
    #         self.fields["owned_game"] = forms.ModelChoiceField(
    #             label="Jeu",
    #             empty_label="",
    #             queryset=OwnedGame.objects.filter(user=user),
    #         )
    #         self.fields["borrower"] = forms.ModelChoiceField(
    #             label="Ami",
    #             empty_label="",
    #             queryset=Friends.objects.filter(user=user),
    #             required=False,
    #         )
    #
    #     game = None
    #     borrower = None
    #     unknown_borrower = forms.CharField(
    #         label="Emprunteur", max_length=100, required=False
    #     )

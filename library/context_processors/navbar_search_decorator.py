"""Decorator to handle navbar_search"""
from django.shortcuts import redirect
from django.urls import reverse

from library.forms import SearchGameForm


def navbar_search_decorator(function):
    """Decorator to add navbar_search form by decorator"""

    def wrapper(*args, **kwargs):
        if args[0].method == "POST":
            if args[0].POST.get("game"):
                form: SearchGameForm = SearchGameForm(args[0].POST)

                if form.is_valid():
                    return redirect(
                        reverse(
                            "library:results",
                            kwargs={
                                "platform": form.cleaned_data["platform"],
                                "query": form.cleaned_data["game"],
                            },
                        )
                    )

        return function(*args, **kwargs)

    return wrapper

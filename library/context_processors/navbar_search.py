"""Pass navbar to context_processors"""
from library.forms import SearchGameForm


def navbar_search(request):
    """Pass toolbar to all views"""
    navbar_form: SearchGameForm = SearchGameForm(request.POST)

    return {"navbar_form": navbar_form}

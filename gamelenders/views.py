"""Accounts views"""
from django.shortcuts import render

from library.context_processors.navbar_search_decorator import navbar_search_decorator


@navbar_search_decorator
def home(request):
    """load homepage"""
    return render(request, "home.html")


@navbar_search_decorator
def legal_notice(request):
    """View for legal notice page"""
    return render(request, "notice.html")

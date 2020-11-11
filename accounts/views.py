"""Accounts views"""
from django.shortcuts import render


def login(request):
    """load login"""
    return render(request, "login.html")

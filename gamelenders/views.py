"""Accounts views"""
from django.shortcuts import render


def home(request):
    """load homepage"""
    return render(request, "home.html")

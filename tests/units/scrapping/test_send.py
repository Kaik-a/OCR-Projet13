"""Test on sending requests"""
from django.test import TestCase

from scrapping import send_requests


class TestSendRequest(TestCase):
    """Class to test requests"""

    send_requests.send_request(query="final fantasy", resources="game")

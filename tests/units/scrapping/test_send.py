"""Test on sending requests"""
from django.test import TestCase

from scrapping import send_requests


class TestSendRequest(TestCase):
    """Class to test requests"""

    # TODO: verify headers
    send_requests.send_request(query="final fantasy", resources="game")

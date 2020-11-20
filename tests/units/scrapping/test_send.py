"""Test on sending requests"""
from unittest.mock import Mock, patch

import requests
from django.test import TestCase

from scrapping import send_requests


class TestSendRequest(TestCase):
    """Class to test requests"""

    def setUp(self) -> None:
        """Test setup"""
        self.patch = None

    def tearDown(self) -> None:
        """Test teardown"""
        try:
            self.patch.stop()
        except AttributeError:
            return

    def get_headers(self, *args, **kwargs) -> requests.Response:
        """Get headers from request"""
        modified_dict = requests.Response()
        mock = Mock(return_value={"results": kwargs.get("headers")})
        self.patch = patch("requests.Response.json", mock)
        self.patch.start()
        return modified_dict

    def test_headers(self):
        """Test if headers in request"""
        patch_request = patch("requests.get", self.get_headers)

        patch_request.start()

        headers = send_requests.send_request(query="final fantasy", resources="game")

        self.assertEqual(
            headers,
            {
                "User-Agent": "gamelenders",
            },
        )

        patch_request.stop()

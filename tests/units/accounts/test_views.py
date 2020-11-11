"""Test accounts views"""
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    """class to test accounts views"""

    def test_login_view(self):
        """Load login view"""

        url = reverse("accounts:login")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

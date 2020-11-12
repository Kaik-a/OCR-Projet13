"""Test on account module's views"""
from django.urls import reverse

from tests.test_pattern import TestPattern


class TestViews(TestPattern):
    """Tests on ocrProjet views."""

    def test_login(self):
        """Load login"""
        url = reverse("accounts:login")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Load logout"""
        url = reverse("accounts:logout")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_subscription(self):
        """Load subscription"""
        url = reverse("accounts:subscription")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_account(self):
        """Load user accounts"""
        url = reverse("accounts:user_account")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_check_mail(self):
        """Load check mail"""
        url = reverse("accounts:check_mail")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_send_reset(self):
        """Load send reset"""
        url = reverse("accounts:send_reset", args=[self.user.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_reset_password(self):
        """Load reset password"""
        url = reverse("accounts:reset_password", args=[self.user.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_validate_password(self):
        """Load validate on password"""
        url = reverse("accounts:validate", args=[self.awaiting_data_1.guid])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.request["PATH_INFO"],
            "/accounts/validate/" + str(self.awaiting_data_1.guid),
        )

    def test_validate(self):
        """Load validate on subscription"""
        url = reverse("accounts:validate", args=[self.awaiting_data_2.guid])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.request["PATH_INFO"],
            "/accounts/validate/" + str(self.awaiting_data_2.guid),
        )

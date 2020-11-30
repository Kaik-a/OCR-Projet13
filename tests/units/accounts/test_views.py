"""Test on account module's views"""
from uuid import uuid4

from django.urls import reverse

from accounts.models import AwaitingData
from tests.test_pattern import TestPattern


class TestViews(TestPattern):
    """Tests on ocrProjet views."""

    def setUp(self) -> None:
        super().setUp()

        self.awaiting_data_1 = AwaitingData(
            guid=uuid4(), type="password", key="password", value="1234"
        )

        self.awaiting_data_1.save()

        self.uuid_subscription = uuid4()
        self.awaiting_data_2 = AwaitingData(
            guid=self.uuid_subscription,
            type="subscription",
            key="login",
            value="test_login",
        )

        awaiting_subscription = [
            self.awaiting_data_2,
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="first_name",
                value="test_first_name",
            ),
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="last_name",
                value="test_last_name",
            ),
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="email",
                value="test2@test.com",
            ),
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="password",
                value="12345",
            ),
        ]

        for data in awaiting_subscription:
            data.save()

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

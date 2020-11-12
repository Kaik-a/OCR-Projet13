"""Test pattern for other test"""
from unittest.mock import patch
from uuid import uuid4

from django.test import RequestFactory, TestCase

from accounts.models import AwaitingData, CustomUser


class TestPattern(TestCase):
    """Global set up"""

    def setUp(self) -> None:
        """Environment for tests"""
        self.factory = RequestFactory()
        self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")

        self.user = CustomUser.objects.create_user(
            username="test1", password="test1@1234", email="test@test.com"
        )

        self.client.login(username="test1", password="test1@1234")

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

        self.stop_messages = patch("django.contrib.messages.add_message").start()

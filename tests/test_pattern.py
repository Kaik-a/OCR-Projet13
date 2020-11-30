"""Test pattern for other test"""
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from accounts.models import CustomUser


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

        self.stop_messages = patch("django.contrib.messages.add_message").start()

        self.user2 = CustomUser.objects.create_user(
            username="test2", password="test2@1234", email="test2@test.com"
        )

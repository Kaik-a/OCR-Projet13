"""Tests to see if mails are correctly sent"""
from django.core import mail

from accounts.commands.commands import mail_password, mail_subscription
from tests.test_pattern import TestPattern


class TestMail(TestPattern):
    """Class to test mails"""

    def test_subscription(self):
        """Test mail sent on subscription"""
        data = {
            "login": "test_login",
            "last_name": "test_last_name",
            "first_name": "test_first_name",
            "email": "test@mail.com",
            "password": "test_password",
            "confirm_password": "test_password",
        }
        mail_subscription(self.factory, data)

        assert len(mail.outbox) == 1

        self.assertEqual(mail.outbox[0].subject, "Création de compte")

    def test_reset_password(self):
        """Test mail sent when resetting password"""
        mail_password(self.factory, self.user.id)

        assert len(mail.outbox) == 1

        self.assertEqual(mail.outbox[0].subject, "Changement de mot de passe")

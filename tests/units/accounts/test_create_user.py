"""Test while creating user"""
from django.db import IntegrityError
from django.test import TestCase

from accounts.models import CustomUser


class CreateUserTest(TestCase):
    """Class to test create user"""

    def test_email_unique(self):
        """Test only one account can be created with same email"""

        CustomUser.objects.create_user(
            username="test_1", email="test_1@test.com", password="test"
        )

        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="test_2", email="test_1@test.com", password="test"
            )

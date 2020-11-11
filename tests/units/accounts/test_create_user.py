"""Test while creating user"""
from django.test import TestCase


class CreateUserTest(TestCase):
    """Class to test create user"""

    def test_email_unique(self):
        """Test only one account can be created with same email"""

        ...

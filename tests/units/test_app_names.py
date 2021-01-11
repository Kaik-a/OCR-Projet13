"""Assure app name stay same"""
from django.test import TestCase

from accounts.apps import AccountsConfig
from library.apps import LibraryConfig
from scrapping.apps import ScrappingConfig


class TestAppName(TestCase):
    """Test App names"""

    def test_accounts(self):
        """Make sure appname is correct"""
        self.assertEqual(AccountsConfig.name, "accounts")

    def test_library(self):
        """Make sure appname is correct"""
        self.assertEqual(LibraryConfig.name, "library")

    def test_scrapping(self):
        """Make sure appname is correct"""
        self.assertEqual(ScrappingConfig.name, "scrapping")

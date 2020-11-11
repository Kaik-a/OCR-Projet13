"""Test on account module's form"""
from django.test import TestCase

from accounts.forms import ChangePasswordForm, CheckMailForm, LoginForm, SubscribeForm


class TestForms(TestCase):
    """Test on accounts forms"""

    def test_login_form(self):
        """Test login form"""
        form = LoginForm(data={"login": "test_user", "password": "test_password"})

        assert form.is_valid()

    def test_subscribe_form(self):
        """Test subscribe form"""
        data = {
            "login": "test_login",
            "last_name": "test_last_name",
            "first_name": "test_first_name",
            "email": "test@mail.com",
            "password": "test_password",
            "confirm_password": "test_password",
        }

        assert SubscribeForm(data=data).is_valid()

        data.update(confirm_password="test")

        assert not SubscribeForm(data=data).is_valid()

    def test_check_mail_form(self):
        """Test check mail form"""
        form = CheckMailForm(data={"email": "test@test.com"})

        assert form.is_valid()

    def test_change_password_form(self):
        """Test change password form"""
        data = {"new_password": "1234", "confirm_new_password": "1234"}

        assert ChangePasswordForm(data=data).is_valid()

        data.update(confirm_new_password="123")

        assert not ChangePasswordForm(data=data).is_valid()

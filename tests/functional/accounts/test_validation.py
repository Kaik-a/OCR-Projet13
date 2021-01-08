"""Test validation"""
import re

from django.core import mail
from selenium import webdriver

from tests.functional.test_selenium import SeleniumBasedTestCase


class TestValidation(SeleniumBasedTestCase):
    """Test validation"""

    def test_create_account(self):
        """An user can be created passing by subscription"""
        self.driver.get(self.live_server_url)

        # load subscription
        self.driver.find_element_by_id("subscription").click()

        self.assertEqual(self.driver.title, "Inscription")

        # fill form
        self.driver.find_element_by_id("id_login").send_keys("test_selenium")

        self.driver.find_element_by_id("id_last_name").send_keys(
            "test_selenium_last_name"
        )

        self.driver.find_element_by_id("id_first_name").send_keys(
            "test_selenium_first_name"
        )

        self.driver.find_element_by_id("id_email").send_keys(
            "test_selenium_email@test.com"
        )

        self.driver.find_element_by_id("id_password").send_keys(
            "test_selenium_password"
        )

        self.driver.find_element_by_id("id_confirm_password").send_keys(
            "test_selenium_password"
        )

        # validate form
        self.driver.find_element_by_id("subscribe_button").click()

        self.assertEqual(self.driver.title, "Login")

        # a mail is out
        assert mail.outbox

        driver_2 = make_validation(self)

        driver_2.close()

        # log in
        self.driver.find_element_by_id("id_login").send_keys("test_selenium")

        self.driver.find_element_by_id("id_password").send_keys(
            "test_selenium_password"
        )

        self.driver.find_element_by_id("login-button").click()

        self.assertEqual(self.driver.title, "Compte")

    def test_reset_password(self):
        """A given user can reset his password"""
        self.driver.get(self.live_server_url)

        # load login
        self.driver.find_element_by_id("navbar_account").click()

        # password forgotten
        self.driver.find_element_by_id("forgot_password").click()

        # fill email
        self.driver.find_element_by_id("id_email").send_keys("test@test.com")

        self.driver.find_element_by_id("send_mail").click()

        # mail out
        assert mail.outbox

        driver_2 = make_validation(self)

        # fill new password
        driver_2.find_element_by_id("id_new_password").send_keys("new_password")

        driver_2.find_element_by_id("id_confirm_new_password").send_keys("new_password")

        driver_2.find_element_by_id("reset_password_button").click()

        self.assertEqual(driver_2.title, "Login")

        # log in
        driver_2.find_element_by_id("id_login").send_keys("test1")

        driver_2.find_element_by_id("id_password").send_keys("new_password")

        driver_2.find_element_by_id("login-button").click()

        self.assertEqual(driver_2.title, "Compte")

        driver_2.close()


def make_validation(test_case: SeleniumBasedTestCase) -> webdriver.Firefox:
    """Make action's validation

    :param: test_case: SeleniumBasedTestCase
    :rtype: webdriver.Firefox
    """
    pattern = "/accounts.*"

    # link to validate is in mail
    validate = re.findall(pattern, mail.outbox[0].body)[0]

    driver_2 = webdriver.Firefox(
        capabilities=test_case.caps,
        firefox_binary=test_case.binary,
    )

    # validate
    driver_2.get(test_case.live_server_url + validate)

    return driver_2

"""Test on friends"""
from django.core.exceptions import ObjectDoesNotExist
from selenium.webdriver.support.select import Select

from accounts.models import Friends
from tests.functional.test_selenium import SeleniumBasedTestCase


class TestFriends(SeleniumBasedTestCase):
    """Test on friends"""

    def test_delete_friend(self):
        """An authenticated user should be able to delete friends"""
        self.driver.get(self.live_server_url + "/accounts/login")

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        self.driver.find_element_by_id("friends-button").click()

        self.assertEqual(self.driver.title, "Amis")

        # make sure user have a friend
        self.assertTrue(Friends.objects.get(user=self.user))

        # delete friend
        self.driver.find_element_by_class_name("btn-danger").click()

        with self.assertRaises(ObjectDoesNotExist):
            Friends.objects.get(user=self.user)

    def test_add_friend(self):
        """An authenticated user should be able to add friends"""
        Friends.objects.all().delete()

        self.driver.get(self.live_server_url + "/accounts/login")

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        self.driver.find_element_by_id("friends-button").click()

        self.assertEqual(self.driver.title, "Amis")

        with self.assertRaises(ObjectDoesNotExist):
            Friends.objects.get(user=self.user)

        Select(self.driver.find_element_by_id("search-friend-form")).select_by_index(1)

        self.driver.find_element_by_id("add-friend-button").click()

        # assert user now have a friend
        self.assertTrue(Friends.objects.get(user=self.user))

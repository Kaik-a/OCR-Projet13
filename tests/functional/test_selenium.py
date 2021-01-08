# """Selenium based tests"""
# import re
# from datetime import datetime
# from uuid import uuid4
#
# from catalog.models import Favorite, Product
# from django.core import mail
# from django.test import LiveServerTestCase
# from pytest import raises
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver import DesiredCapabilities
# from selenium.webdriver.common.keys import Keys
#
# from accounts.models import CustomUser

#
# class SeleniumBasedTestCase(LiveServerTestCase):
#     """Test based on Selenium."""
#
#     def setUp(self) -> None:
#         """Set up tets environment"""
#         self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
#
#         self.caps = DesiredCapabilities().FIREFOX.copy()
#         self.caps["marionette"] = True
#         self.binary = (
#             "/Applications/Applications/Firefox.app/Contents/" "MacOS/firefox-bin"
#         )
#
#         self.user = CustomUser.objects.create_user(
#             username="test1", password="test1@1234", email="test@test.com"
#         )
#
#         self.driver = webdriver.Firefox(
#             capabilities=self.caps,
#             firefox_binary=self.binary,
#         )
#
#         self.driver.implicitly_wait(10)
#
#         self.product_1 = Product(
#             id=uuid4(),
#             product_name_fr="produit bon",
#             nutrition_grade_fr="A",
#             categories_tags=["Pâte à tartiner"],
#         )
#         self.product_2 = Product(**NUTELLA)
#
#         self.product_1.save()
#         self.product_2.save()
#
#     def tearDown(self) -> None:
#         """Method to call at teardown."""
#         self.driver.close()
#
#     def test_save_favorite(self):
#         """An authenticated user should be able to save favorites."""
#         self.driver.get(self.live_server_url + "/accounts/login")
#
#         # login
#         self.driver.find_element_by_id("id_login").send_keys(self.user.username)
#         self.driver.find_element_by_id("id_password").send_keys("test1@1234")
#         self.driver.find_element_by_id("login-button").click()
#
#         # go to home page
#         self.driver.find_element_by_id("pur-beurre").click()
#
#         self.assertEqual(self.driver.title, "Pur beurre")
#
#         # select search form
#         self.driver.find_element_by_class_name("select2-selection").click()
#
#         # search for a product
#         self.driver.find_element_by_class_name("select2-search__field").send_keys(
#             Keys.ENTER
#         )
#
#         # click on "chercher" button
#         self.driver.find_element_by_id("search-button").click()
#
#         self.assertEqual(self.driver.title, "Résultats")
#
#         self.assertEqual(len(Favorite.objects.all().filter(user=self.user)), 0)
#
#         # save first product
#         self.driver.find_element_by_xpath("//figure/form/button").click()
#
#         # go to favorites
#         self.driver.find_element_by_id("carrot-logo").click()
#
#         self.assertEqual(len(Favorite.objects.all().filter(user=self.user)), 1)
#
#         self.assertEqual(self.driver.title, "Favoris")
#
#     def test_delete_favorite(self):
#         """An authenticated user should be able to delete favorites."""
#         Favorite(
#             substitute=self.product_1,
#             substitued=self.product_2,
#             user=self.user,
#             date=datetime.now(),
#         ).save()
#
#         self.driver.get(self.live_server_url + "/accounts/login")
#
#         # login
#         self.driver.find_element_by_id("id_login").send_keys(self.user.username)
#         self.driver.find_element_by_id("id_password").send_keys("test1@1234")
#         self.driver.find_element_by_id("login-button").click()
#
#         # go to favorites
#         self.driver.find_element_by_id("carrot-logo").click()
#
#         self.assertEqual(self.driver.title, "Favoris")
#
#         self.assertEqual(len(Favorite.objects.all().filter(user=self.user)), 1)
#
#         # delete first product
#         self.driver.find_element_by_xpath("//figure/form/button").click()
#
#         self.assertEqual(len(Favorite.objects.all().filter(user=self.user)), 0)
#
#     def test_fail_access_favorite(self):
#         """An user non authenticated shouldn't access to favorites."""
#         self.driver.get(self.live_server_url)
#
#         # cannot find favorites
#         with raises(NoSuchElementException):
#             self.driver.find_element_by_id("navbar_favorites")
#
#     def test_fail_access_user_account(self):
#         """An user non authenticated shouldn't access to user_account."""
#         self.driver.get(self.live_server_url)
#
#         # click on user accounts
#         self.driver.find_element_by_id("navbar_account").click()
#
#         self.assertEqual(self.driver.title, "Login")
#
#     def test_create_account(self):
#         """An user can be created passing by subscription"""
#         self.driver.get(self.live_server_url)
#
#         # load login
#         self.driver.find_element_by_id("navbar_account").click()
#
#         self.assertEqual(self.driver.title, "Login")
#
#         # load subscription
#         self.driver.find_element_by_id("subscription").click()
#
#         self.assertEqual(self.driver.title, "Inscription")
#
#         # fill form
#         self.driver.find_element_by_id("id_login").send_keys("test_selenium")
#
#         self.driver.find_element_by_id("id_last_name").send_keys(
#             "test_selenium_last_name"
#         )
#
#         self.driver.find_element_by_id("id_first_name").send_keys(
#             "test_selenium_first_name"
#         )
#
#         self.driver.find_element_by_id("id_email").send_keys(
#             "test_selenium_email@test.com"
#         )
#
#         self.driver.find_element_by_id("id_password").send_keys(
#             "test_selenium_password"
#         )
#
#         self.driver.find_element_by_id("id_confirm_password").send_keys(
#             "test_selenium_password"
#         )
#
#         # validate form
#         self.driver.find_element_by_id("subscribe_button").click()
#
#         self.assertEqual(self.driver.title, "Login")
#
#         # a mail is out
#         assert mail.outbox
#
#         driver_2 = make_validation(self)
#
#         driver_2.close()
#
#         # log in
#         self.driver.find_element_by_id("id_login").send_keys("test_selenium")
#
#         self.driver.find_element_by_id("id_password").send_keys(
#             "test_selenium_password"
#         )
#
#         self.driver.find_element_by_id("login-button").click()
#
#         self.assertEqual(self.driver.title, "Compte")
#
#     def test_reset_password(self):
#         """A given user can reset his password"""
#         self.driver.get(self.live_server_url)
#
#         # load login
#         self.driver.find_element_by_id("navbar_account").click()
#
#         # password forgotten
#         self.driver.find_element_by_id("forgot_password").click()
#
#         # fill email
#         self.driver.find_element_by_id("id_email").send_keys("test@test.com")
#
#         self.driver.find_element_by_id("send_mail").click()
#
#         # mail out
#         assert mail.outbox
#
#         driver_2 = make_validation(self)
#
#         # fill new password
#         driver_2.find_element_by_id("id_new_password").send_keys("new_password")
#
#         driver_2.find_element_by_id("id_confirm_new_password").send_keys("new_password")
#
#         driver_2.find_element_by_id("reset_password_button").click()
#
#         self.assertEqual(driver_2.title, "Login")
#
#         # log in
#         driver_2.find_element_by_id("id_login").send_keys("test1")
#
#         driver_2.find_element_by_id("id_password").send_keys("new_password")
#
#         driver_2.find_element_by_id("login-button").click()
#
#         self.assertEqual(driver_2.title, "Compte")
#
#         driver_2.close()
#
#
# def make_validation(test_case: SeleniumBasedTestCase) -> webdriver.Firefox:
#     """Make action's validation
#
#     :param: test_case: SeleniumBasedTestCase
#     :rtype: webdriver.Firefox
#     """
#     pattern = "/accounts.*"
#
#     # link to validate is in mail
#     validate = re.findall(pattern, mail.outbox[0].body)[0]
#
#     driver_2 = webdriver.Firefox(
#         capabilities=test_case.caps,
#         firefox_binary=test_case.binary,
#     )
#
#     # validate
#     driver_2.get(test_case.live_server_url + validate)
#
#     return driver_2

"""Tests on games"""
from django.core.exceptions import ObjectDoesNotExist
from selenium.webdriver.support.select import Select

from library.models import LendedGame, OwnedGame, WantedGame
from tests.functional.test_selenium import SeleniumBasedTestCase


class TestGames(SeleniumBasedTestCase):
    """Tests on games"""

    def test_consult_games(self):
        """An authenticated user should be able to consult his games."""
        self.driver.get(self.live_server_url + "/accounts/login")

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        # go to your games
        self.driver.find_element_by_id("dropdown-list").click()
        self.driver.find_element_by_id("your-games-button").click()

        self.assertEqual(self.driver.title, "Vos jeux")

        # go to game
        self.driver.find_element_by_xpath("//table/tbody/tr/td/a").click()

        self.assertEqual(self.driver.title, self.game.name)

    def test_get_back_game(self):
        """Get back a lended game"""
        self.driver.get(self.live_server_url + "/accounts/login")

        # make sure game was lended
        self.assertTrue(
            LendedGame.objects.get(owned_game=self.owned_game, returned=False)
        )

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        # go to your games
        self.driver.find_element_by_id("dropdown-list").click()
        self.driver.find_element_by_id("your-games-button").click()

        self.assertEqual(self.driver.title, "Vos jeux")

        # make game as returned
        self.driver.find_element_by_xpath("//table/tbody/tr/td[3]/div/a").click()

        # make sure game is returned
        with self.assertRaises(ObjectDoesNotExist):
            LendedGame.objects.get(owned_game=self.owned_game, returned=False)

    def test_lend_game(self):
        """User can lend a game to a friend"""
        self.driver.get(self.live_server_url + "/accounts/login")

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        # go to your games
        self.driver.find_element_by_id("dropdown-list").click()
        self.driver.find_element_by_id("your-games-button").click()

        self.assertEqual(self.driver.title, "Vos jeux")

        # make game as returned
        self.driver.find_element_by_xpath("//table/tbody/tr/td[3]/div/a").click()

        # make sure game is returned
        with self.assertRaises(ObjectDoesNotExist):
            LendedGame.objects.get(owned_game=self.owned_game, returned=False)

        # lend the game
        self.driver.find_element_by_id("lend-a-game").click()
        Select(self.driver.find_element_by_id("id_owned_game")).select_by_index(1)
        Select(self.driver.find_element_by_id("id_borrower")).select_by_index(1)

        self.driver.find_element_by_id("validate-lend").click()

        self.assertTrue(
            LendedGame.objects.get(owned_game=self.owned_game, returned=False)
        )

        # make sure the game can be borrowed twice
        lended_games = len(LendedGame.objects.all())

        self.driver.find_element_by_id("lend-a-game").click()
        Select(self.driver.find_element_by_id("id_owned_game")).select_by_index(1)
        Select(self.driver.find_element_by_id("id_borrower")).select_by_index(1)

        self.driver.find_element_by_id("validate-lend").click()

        self.assertEqual(len(LendedGame.objects.all()), lended_games)

    def test_consult_borrowed_games(self):
        """An authenticated user should be able to consult his borrowed games."""
        self.driver.get(self.live_server_url + "/accounts/login")

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        # go to your borrowed games
        self.driver.find_element_by_id("dropdown-list").click()
        self.driver.find_element_by_id("borrowed-button").click()

        self.assertEqual(self.driver.title, "Jeux empruntés")

    def test_delete_game_from_wishlist(self):
        """An authenticated user should be able to delete games from wishlist."""
        self.driver.get(self.live_server_url + "/accounts/login")

        # make sure there's a wanted game
        self.assertTrue(WantedGame.objects.all())

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        # go to your wish list
        self.driver.find_element_by_id("dropdown-list").click()
        self.driver.find_element_by_id("wanted-button").click()

        self.assertEqual(self.driver.title, "Liste d'envies")

        self.driver.find_element_by_class_name("btn-danger").click()

        # verify there's no more games in wanted list
        self.assertFalse(WantedGame.objects.all())

    def test_delete_game_from_library(self):
        """An authenticated user should be able to delete game from his library."""
        self.driver.get(self.live_server_url + "/accounts/login")

        # make sure game was lended
        self.assertTrue(OwnedGame.objects.all())

        # login
        self.driver.find_element_by_id("id_login").send_keys(self.user.username)
        self.driver.find_element_by_id("id_password").send_keys("test1@1234")
        self.driver.find_element_by_id("login-button").click()

        # go to your games
        self.driver.find_element_by_id("dropdown-list").click()
        self.driver.find_element_by_id("your-games-button").click()

        self.assertEqual(self.driver.title, "Vos jeux")

        # make game as returned
        self.driver.find_element_by_xpath("//table/tbody/tr/td[3]/div/a").click()

        # delete game from library
        self.driver.find_element_by_class_name("btn-danger").click()

        self.assertFalse(OwnedGame.objects.all())

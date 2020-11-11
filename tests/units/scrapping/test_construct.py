"""Test on constructs"""
from django.test import TestCase

from scrapping import API_KEY, construct_requests


class TestConstruct(TestCase):
    """Class to test constructs."""

    def test_construct_query(self):
        """Make sure queries are constructed correctly."""
        query = construct_requests.add_query("Final Fantasy")

        self.assertEqual(query, '&query="final fantasy"')

    def test_construct_resources(self):
        """Make sure resources are constructed correctly"""
        resources_1 = construct_requests.add_resources(["games", "platform"])

        self.assertEqual(resources_1, "&resources=games,platform")

        resources_2 = construct_requests.add_resources("genre")

        self.assertEqual(resources_2, "&resources=genre")

    def test_construct_data_format(self):
        """Make sure data_format are constructed correctly"""
        data_format = construct_requests.add_data_format("JSON")

        self.assertEqual(data_format, "&format=json")

    def test_construct_request(self):
        """Make sure requests are constructed correctly"""
        base = "http://www.giantbomb.com/api/search/?api_key=" + API_KEY

        # verify constrct request only accept keyword arguments
        with self.assertRaises(TypeError):
            # pylint: disable=E1121,E1125
            construct_requests.construct_request("Final Fantasy", "json", "game")

        request_1 = construct_requests.construct_request(query="Final Fantasy")

        self.assertEqual(request_1, base + '&format=json&query="final fantasy"')

        request_2 = construct_requests.construct_request(
            query="final fantasy", data_format="xml"
        )

        self.assertEqual(request_2, base + '&format=xml&query="final fantasy"')

        request_3 = construct_requests.construct_request(
            query="final Fantasy", resources=["games", "platform"]
        )

        self.assertEqual(
            request_3,
            base + '&format=json&query="final fantasy"&resources=games,platform',
        )

        request_4 = construct_requests.construct_request(
            query="FINAL FANTASY", data_format="xml", resources="games"
        )

        self.assertEqual(
            request_4, base + '&format=xml&query="final fantasy"&resources=games'
        )

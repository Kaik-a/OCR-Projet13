"""Constants for scrapping"""
import os

BASE_URL = "http://www.giantbomb.com/api/"
API_KEY = os.environ["GIANTBOMB"]
SEARCH_PATTERN = BASE_URL + "search/?api_key=" + API_KEY

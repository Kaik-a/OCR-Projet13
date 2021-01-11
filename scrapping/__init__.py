"""Constants for scrapping"""
import os

BASE_URL = "http://www.giantbomb.com/api/"
API_KEY = "?api_key=" + os.environ["GIANTBOMB"]
SEARCH_PATTERN = BASE_URL + "search/" + API_KEY

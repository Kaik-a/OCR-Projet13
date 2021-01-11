"""Construct request for giantbomb API"""
from typing import List, Union

from scrapping import API_KEY, BASE_URL, SEARCH_PATTERN


def construct_request(
    *, query: str, data_format: str = "json", resources: Union[List[str], str] = None
) -> str:
    """
    Construct request to search through giantbomb api.

    :param str query: query to look for
    :param str data_format: format of data returned by the API
    :param str, List[str] resources: type of resources searched
    :rtype: str
    """
    search_query = SEARCH_PATTERN + add_data_format(data_format) + add_query(query)

    if resources:
        search_query += add_resources(resources)

    return search_query


def add_data_format(data_format: str) -> str:
    """
    Add format to request.

    :param str data_format: format of data returned by the API
    :rtype: str
    """
    return f"&format={data_format.lower()}"


def add_query(query: str) -> str:
    """
    Add query to request.

    :param str query: query to look for
    :rtype: str
    """
    return f'&query="{query.lower()}"'


def add_resources(resources: Union[List[str], str]) -> str:
    """
    Add types of resources to request.

    :param str, List[str] resources: type of resources searched
    :rtype: str
    """
    base = "&resources="

    if isinstance(resources, str):
        return base + resources.lower()

    return base + ",".join([resource.lower() for resource in resources])


def construct_platform_request() -> str:
    """Construct platform request to populate the DB"""
    request = BASE_URL + "platforms/" + API_KEY
    request += add_data_format("json")

    return request

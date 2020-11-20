"""Send request to giantbomb API"""
from typing import List, Union

import requests

from scrapping import construct_requests


def send_request(
    *, query: str, data_format: str = "json", resources: Union[List[str], str] = None
) -> List:
    """
    Send request to giantbomb API.

    :param str query: query to look for
    :param str data_format: format of data returned by the API
    :param List[str] resources: type of resources searched
    :rtype: List
    """

    # headers are needed to identify to giantbom API otherwise, API throw a 403 error
    headers = {
        "User-Agent": "gamelenders",
    }

    request = requests.get(
        construct_requests.construct_request(
            query=query, data_format=data_format, resources=resources
        ),
        headers=headers,
    )

    return request.json()["results"]


def get_platforms():
    """Get platforms from GiantBomb"""
    headers = {"User-Agent": "gamelenders"}

    url: str = construct_requests.construct_platform_request()

    request = requests.get(
        url,
        headers=headers,
    )

    return request.json()["results"]

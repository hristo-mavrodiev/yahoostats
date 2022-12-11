"""
Webscraping using requests.get function and BeautifulSoup.
Without Firefox Chrome or Selenium.
"""

import requests
from bs4 import BeautifulSoup as soup
from time import sleep
from tenacity import retry
from tenacity import wait_fixed, stop_after_attempt
import json
from pprint import pprint as pp
from typing import Union
import logging
logger = logging.getLogger(__name__)


Response = requests.models.Response

@retry(wait=wait_fixed(3), stop=stop_after_attempt(3))
def get_page_content(url: str) -> Union[Response, None]:
    """Function to get data from url with retry between attempts.

    Parameters
    ----------
    url : str
        valid URL address

    Returns
    -------
    requests.models.Response | None
        raw data from the URL or None
    """
    logger.debug(f'Fetching url: {url}')
    result = None
    try:
        result = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
    except Exception as exe:
        logger.error(f"Unable to load the url {exe}")
    return result





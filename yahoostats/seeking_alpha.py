
import requests
from bs4 import BeautifulSoup as soup
from time import sleep
from tenacity import retry
from tenacity import wait_fixed, stop_after_attempt
import json
from pprint import pprint as pp
from typing import Union
from yahoostats.utils import get_page_content
import logging
logger = logging.getLogger(__name__)



def seeking_alpha(ticker):
    """
    URL https://seekingalpha.com/symbol/INTC/ratings/analysis_summary_data

    TODO: https://seekingalpha.com/api/v3/symbols/amd/rating/histories?page[number]=1
    """
    url = f"https://seekingalpha.com/symbol/{ticker}/ratings/analysis_summary_data"
    logger.info(f'-----Seeking alpha-----')
    logger.info(f'Fetching data for {ticker}')
    logger.debug(f'Using requests on {url}')
    sa_rating = None
    sa_target_price = None
    try:
        resp = get_page_content(url)
        data = resp.json()
        sa_rating = data['data']['rating']
        sa_target_price = data['data']['target_price']
    except Exception as exe:
        logger.warning(f'Unable to get data from seeking_alpha {exe} - {url}')
    return {'sa_rating': sa_rating, 'sa_target_price': sa_target_price}

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


# def zacks_stats(ticker):
#     """
#     Get Zacks start rating for specific stock.
#     https://www.zacks.com/stock/chart/GTT/fundamental/peg-ratio-ttm
#     https://www.zacks.com/stock/quote/GOOGL/financial-overview
#     https://www.zacks.com/stock/quote/TSLA/financial-overview

#     <div> class = 'zr_rankbox'
#     <p> class = 'rank_view' .text
#     added sleep for error code#104 on colab
#     https://stackoverflow.com/questions/52051989/requests-exceptions-connectionerror-connection-aborted-connectionreseterro
#     """
#     logger.info('-----Zacks-----')
#     logger.info(f'Fetching data for {ticker}')
#     url = f'https://www.zacks.com/stock/quote/{ticker}/financial-overview'
#     try:
#         sleep(0.01)
#         soup_zack = soup(get_page_content(url).content, "html.parser")
#         rating_div = soup_zack.find('div', {'class': 'zr_rankbox'})
#         rating_label = rating_div.find('p')
#         rating_value = rating_label.text
#     except Exception as exe:
#         logger.warning(f'Unable to get data from zacks {exe}')
#         rating_value = "---"
#     return {'zacks_rate': rating_value.split()[0]}

def zacks_stats(ticker):
    """
    Get Zacks start rating for specific stock.
    URL: https://quote-feed.zacks.com/index?t=INTC
    Inputs:
    --------------------
    Ticker - stock symbol

    Outputs:
    ---------------------------
    Dictionary with:
    "zacks_rate" : zacks_rank - zacks_rank_text
    """
    logger.info('-----Zacks-----')
    logger.info(f'Fetching data for {ticker}')
    url = f'https://quote-feed.zacks.com/index?t={ticker}'
    zacks_rate = None
    ticker = ticker.upper()
    try:
        resp = get_page_content(url)
        data = resp.json()
        rank = data[f'{ticker}']['zacks_rank']
        rank_text = data[f'{ticker}']['zacks_rank_text']
        zacks_rate = f'{rank} - {rank_text}'
    except Exception as exe:
        logger.warning(f'Unable to get data from zacks {exe}')
    return {'zacks_rate': zacks_rate}
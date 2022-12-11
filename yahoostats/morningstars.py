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


def morningstar_stats(ticker):
    """
    Function to get stock stars rrating from MorningStar.
    https://www.morningstar.com/stocks/xnas/googl/valuation
    https://financials.morningstar.com/ratios/r.html?t=0P0000006A&culture=en&platform=sal
    https://financials.morningstar.com/ratios/r.html?t=GOOGL
    https://financials.morningstar.com/ratios/r.html?t=tsla&culture=en&platform=sal

    <div> class ='r_title'
    <span> id ='star_span'

    # Get Tiker from 
    # https://www.morningstar.com/api/v2/stocks/xnas/googl/quote
    https://www.morningstar.com/api/v2/stocks/xnys/t/quote
    https://www.morningstar.com/api/v2/stocks/pinx/gttnq/quote --> 0P0000COBV
    # Second request to get rating from the Tiker
    #TODO https://tools.morningstar.co.uk/uk/stockreport/default.aspx?tab=11&vw=pr&SecurityToken=0P000002HD%5D3%5D0%5DE0WWE%24%24ALL&Id=0P000002HD&
    # https://tools.morningstar.co.uk/uk/stockreport/default.aspx?tab=0&vw=sum&SecurityToken=0P0000006A]3]0]E0WWE&Id=0P0000006A
    """
    url = f"https://financials.morningstar.com/ratios/r.html?t={ticker}&culture=en&platform=sal"
    try:
        soup_ms = soup(get_page_content(url).content, "html.parser")
        logger.info(f'-----Morningstar-----')
        logger.info(f'Fetching data for {ticker}')
        start_rating = soup_ms.find('span', {'id': "star_span"})
        return {'ms_stars': start_rating["class"][0]}
    except Exception as exe:
        logger.warning(exe)
        return {'ms_stars': "---"}
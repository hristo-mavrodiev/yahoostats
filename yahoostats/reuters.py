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



def reuters_stats(ticker):
    """
    Function to get data from Thompson Reuters"
    Input:
    ---------------
    ticker - stock symbol

    Outputs:
    ---------------
    Dictionary with fundamental statistics.

    https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&search="COMPANY"
    https://www.reuters.com/companies/GOOGL.O/key-metrics
    https://www.reuters.com/companies/IBM/key-metrics
    O - NASDAQ
    OQ - NASDAQ Stock Exchange Global Select Market
    N - NEWYORK Stock Exchange
    ""or without specified exchange - NEWYORK CONSOLIDATED
    """
    exchanges = ['', '.OQ', '.O', '.N']
    try:
        for exchange in exchanges:
            url = f"https://www.reuters.com/companies/{ticker}{exchange}/key-metrics/growth"
            used_exchange = ''
            html = soup(get_page_content(url).text, "html.parser")
            title = html.title.text
            logger.info('-----Reuters-----')
            logger.info(f'Trying with {ticker} on {exchange} -> {title}')
            if 'Page Not Found' in title:
                continue
            elif ticker in title:
                soup1 = soup(get_page_content(url).content, "html.parser")
                used_exchange = exchange
                break
        data_dict = {}
        data_dict.update({"exchange": used_exchange})
        for table in soup1.findAll('div', {'class': "KeyMetrics-table-container-3wVZN"}):
            for row in table.findAll("tr"):
                keys = row.findAll('th')
                values = row.findAll("td")
                row = []
                if keys and values and keys[0].text:
                    # print({keys[0].text: values[0].text})
                    data_dict.update({keys[0].text: values[0].text})
    except Exception as exe:
        logger.warning(exe)
        logger.warning(f'Wetsite {url} changed need to edit the function.')
        data_dict = {}
    return data_dict


def filter_reuters(data):
    """
    Filter the data from reuters.
    Input:
    ----------------------
    Data - webscraped data from reuters_stats function

    Output:
    ----------------------
    Dictionary with fundamental statistics
    """
    r_beta = None
    r_eps_gr3 = None
    r_eps_gr5 = None
    r_div_gr3 = None
    r_roi_ttm = None
    r_roi_5 = None
    r_current_ratio = None
    r_mar_cap = None
    r_net_income = None
    r_net_debt = None
    r_div_yield = None
    r_div_yield5 = None
    r_rev_employee = None
    r_eps = None
    try:
        logger.info('-----Reuters data function-----')
        r_beta = data.get('Beta')
        r_eps_gr3 = data.get('EPS Growth Rate (3Y)')
        r_eps_gr5 = data.get('EPS Growth Rate (5Y)')
        r_div_gr3 = data.get('Dividend Growth Rate (3Y)')
        r_roi_ttm = data.get('Return on Investment (TTM)')
        r_roi_5 = data.get('Return on Investment (5Y)')
        r_current_ratio = data.get('Current Ratio (Annual)')
        r_mar_cap = data.get('Market Capitalization')
        r_net_income = data.get(
            'Net Income Available to Common Normalized (Annual)')
        r_net_debt = data.get('Net Debt (Annual)')
        r_div_yield = data.get('Dividend Yield')
        r_div_yield5 = data.get('Dividend Yield (5Y)')
        r_rev_employee = data.get('Revenue/Employee (TTM)')
        r_eps = data.get('EPS Normalized (Annual)')
    except Exception as exe:
        logger.warning(exe)
    filtered = {k: v for k, v in locals().items()
                if not k.startswith('data')}
    return filtered
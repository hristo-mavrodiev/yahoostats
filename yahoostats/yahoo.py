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


def yahoo_api_financials(ticker):
    """
    Get the data from Yahoo API
    Inputs:
    --------------------
    Ticker - stock symbol

    Outputs:
    ---------------------------
    Dictionary with:
    'yf_price_now': current_price,
    'yf_price_target': target_price,
    'yf_ratingvalue': yahoo price rating_value,
    'yf_ratingstring': yahoo price rating_string,
    'yf_profit': yahoo profit on the price,
    'yf_current_ratio': current_ratio,
    'yf_return_assets': return on assets,
    'yf_return_equity': return on equity,
    'yf_beta': beta
    """
    logger.info('-----Yahoo Finance API-----')
    logger.info(f'Fetching data for {ticker}')
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=' \
        + 'financialData%2CdefaultKeyStatistics'
    try:
        resp = get_page_content(url)
        data = resp.json()
        fin_data = data['quoteSummary']['result'][0]['financialData']
        current_price = fin_data['currentPrice'].get('raw')
        target_price = fin_data['targetMeanPrice'].get('raw')
        yahoo_rating_val = fin_data['recommendationMean'].get('raw')
        yahoo_rating_str = fin_data['recommendationKey']
        yahoo_valuation = float(target_price) / float(current_price)
        yahoo_current_ratio = fin_data['currentRatio'].get('raw')
        y_return_assets = fin_data['returnOnAssets'].get('raw')
        y_return_equity = fin_data['returnOnEquity'].get('raw')
        bs_data = data['quoteSummary']['result'][0].get('defaultKeyStatistics')
        beta = bs_data.get('beta').get('raw')
    except Exception:
        beta = None
        y_return_equity, yahoo_current_ratio = None, None
        y_return_assets, yahoo_valuation = None, None
        yahoo_rating_str, yahoo_rating_val = None, None
        target_price, current_price = None, None
    result = {'yf_price_now': current_price,
              'yf_price_target': target_price,
              'yf_ratingvalue': yahoo_rating_val,
              'yf_ratingstring': yahoo_rating_str,
              'yf_profit': yahoo_valuation,
              'yf_current_ratio': yahoo_current_ratio,
              'yf_return_assets': y_return_assets,
              'yf_return_equity': y_return_equity,
              'yf_beta': beta}
    return result
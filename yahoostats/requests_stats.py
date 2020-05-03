import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as soup
from time import sleep
import pickle
import json
from pprint import pprint as pp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# from requests.packages.urllib3.util.retry import Retry


def get_page_content(url):
    """
    Function to get Beautifulsoup from provided url with requests.
    """
    sleep(0.25)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == requests.codes['ok']:
            soup1 = soup(res.content, "html.parser")
            return soup1
    except Exception as exe:
        print(f"Unable to load the url {exe}")
        return None


def reuters_stats(ticker):
    """
    Function to get data from Thompson Reuters"
    https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&search="COMPANY"
    https://www.reuters.com/companies/GOOGL.O/key-metrics
    https://www.reuters.com/companies/IBM/key-metrics
    O - NASDAQ
    OQ - NASDAQ Stock Exchange Global Select Market
    N - NEWYORK Stock Exchange
    ""or without specified exchange - NEWYORK CONSOLIDATED
    """
    exchanges = ['', '.OQ', '.O', '.N']
    for exchange in exchanges:
        url = f"https://www.reuters.com/companies/{ticker}{exchange}/key-metrics"
        s = requests.Session()
        res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
        used_exchange = ''
        if res.status_code == requests.codes['ok']:
            html = soup(res.text, "html.parser")
            title = html.title.text
            print(title)
            if 'Page Not Found' in title:
                continue
            elif ticker in title:
                soup1 = soup(res.content, "html.parser")
                used_exchange = exchange
                break
        soup1 = get_page_content(url)
    try:
        df = {}
        df.update({"exchange": used_exchange})
        for table in soup1.findAll('div', {'class': "KeyMetrics-table-container-3wVZN"}):
            for row in table.findAll("tr"):
                keys = row.findAll('th')
                values = row.findAll("td")
                row = []
                if keys and values and keys[0].text:
                    # print({keys[0].text: values[0].text})
                    df.update({keys[0].text: values[0].text})
    except Exception as exe:
        print(exe)
        print(f'Wetsite {url} changed need to edit the function.')
        df = pd.DataFrame()
    return df


def filter_reuters(data):
    """
    Filter the data from reuters.
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
        print(exe)
    filtered = {k: v for k, v in locals().items()
                if not k.startswith('data')}
    return filtered


def morningstar_stats(ticker):
    """
    Function to get stock stars rrating from MorningStar.
    https://www.morningstar.com/stocks/xnas/googl/valuation
    https://financials.morningstar.com/ratios/r.html?t=0P0000006A&culture=en&platform=sal
    https://financials.morningstar.com/ratios/r.html?t=GOOGL
    https://financials.morningstar.com/ratios/r.html?t=tsla&culture=en&platform=sal

    <div> class ='r_title'
    <span> id ='star_span'
    """
    url = f"https://financials.morningstar.com/ratios/r.html?t={ticker}&culture=en&platform=sal"
    soup_ms = get_page_content(url)
    try:
        start_rating = soup_ms.find('span', {'id': "star_span"})
        return {'ms': start_rating["class"][0]}
    except Exception as exe:
        print(exe)
        return None


def zacks_stats(ticker):
    """
    Get Zacks start rating for specific stock.
    https://www.zacks.com/stock/chart/GTT/fundamental/peg-ratio-ttm
    https://www.zacks.com/stock/quote/GOOGL/financial-overview
    https://www.zacks.com/stock/quote/TSLA/financial-overview

    <div> class = 'zr_rankbox'
    <p> class = 'rank_view' .text
    """
    url = f'https://www.zacks.com/stock/quote/{ticker}/financial-overview'
    soup_zack = get_page_content(url)
    rating_div = soup_zack.find('div', {'class': 'zr_rankbox'})
    rating_label = rating_div.find('p')
    rating_value = rating_label.text
    return {'zacks': rating_value.split()[0]}


def yahoo_api_financials(ticker):
    """
    Get the data from Yahoo API

    """
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=' \
        + 'financialData%2CdefaultKeyStatistics'
    resp = requests.get(url)
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
    try:
        beta = bs_data.get('beta').get('raw')
    except Exception:
        beta = None
    result = {'yf_pr_now': current_price,
              'yf_pr_trg': target_price,
              'yf_rv': yahoo_rating_val,
              'yf_rs': yahoo_rating_str,
              'yf_prof': yahoo_valuation,
              'yf_cur_ratio': yahoo_current_ratio,
              'yf_ret_assets': y_return_assets,
              'yf_ret_equity': y_return_equity,
              'yf_beta': beta}
    return result

"""
Webscraping using requests.get function and BeautifulSoup.
Without Firefox Chrome or Selenium.
"""

import requests
from bs4 import BeautifulSoup as soup
from time import sleep
import json
from pprint import pprint as pp
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
logger = logging.getLogger(__name__)


def get_page_content(url):
    """
    Function to use requests.get on provided url with retry and delay between retries.
    """
    s = requests.Session()
    retries = Retry(total=3,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    logger.debug(f'Fetching url: {url}')
    try:
        sleep(0.01)
        res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == requests.codes['ok']:
            return res
    except Exception as exe:
        logger.error(f"Unable to load the url {exe}")
        return None


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
            url = f"https://www.reuters.com/companies/{ticker}{exchange}/key-metrics"
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
    try:
        soup_ms = soup(get_page_content(url).content, "html.parser")
        logger.info(f'-----Morningstar-----')
        logger.info(f'Fetching data for {ticker}')
        start_rating = soup_ms.find('span', {'id': "star_span"})
        return {'ms_stars': start_rating["class"][0]}
    except Exception as exe:
        logger.warning(exe)
        return {'ms_stars': "---"}


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


def tipranks_price(ticker):
    """
    URL https://market.tipranks.com/api/details/getstockdetailsasync/?&id=AMD
    """
    url_tr = f"https://market.tipranks.com/api/details/getstockdetailsasync/?&id={ticker}"
    logger.info(f'-----Tipranks price-----')
    logger.info(f'Fetching data for {ticker}')
    logger.debug(f'Using requests on {url_tr}')
    tr_price_now = None
    try:
        resp = get_page_content(url_tr)
        data = resp.json()
        tr_price_now = data[0]['price']
    except Exception as exe:
        logger.warning(f'Unable to get data from tipranks_price {exe} - {url_tr}')
    return {'tr_price_now': tr_price_now}


def tipranks_analysis(ticker):
    """
    URL https://www.tipranks.com/api/stocks/stockAnalysisOverview/?tickers=AMD
    """
    url_tr = f"https://www.tipranks.com/api/stocks/stockAnalysisOverview/?tickers={ticker}"
    logger.info(f'-----Tipranks analysis-----')
    logger.info(f'Fetching data for {ticker}')
    logger.debug(f'Using requests on {url_tr}')
    tr_score = None
    tr_Fundamentals_ROE = None
    tr_Fundamentals_Grow = None
    tr_Technicals = None
    tr_AnalystRatings = None
    tr_HedgeFundActivity = None
    tr_InsiderActivity = None
    tr_TipRanksInvestors = None
    tr_NewsSentiment = None
    tr_BloggerOpinions = None
    tr_target_pr = None
    try:
        resp = get_page_content(url_tr)
        data = resp.json()
        tr_score = data[0]['smartScore']
        tr_Fundamentals_ROE = data[0]['fundamentalsReturnOnEquity']
        tr_Fundamentals_Grow = data[0]['fundamentalsAssetGrowth']
        tr_Technicals = data[0]['sma']
        tr_AnalystRatings = data[0]['analystConsensus']
        tr_HedgeFundActivity = data[0]['hedgeFundTrend']
        tr_InsiderActivity = data[0]['insiderTrend']
        tr_TipRanksInvestors = data[0]['investorSentiment']
        tr_NewsSentiment = data[0]['newsSentiment']
        tr_BloggerOpinions = data[0]['bloggerConsensus']
        tr_target_pr = data[0]['priceTarget']
    except Exception as exe:
        logger.warning(f'Unable to get data from tipranks_price {exe} - {url_tr}')
    return {'tr_score': tr_score, 'tr_Fundamentals_ROE': tr_Fundamentals_ROE,
            'tr_Fundamentals_Grow': tr_Fundamentals_Grow, 'tr_Technicals': tr_Technicals,
            'tr_AnalystRatings': tr_AnalystRatings, 'tr_HedgeFundActivity': tr_HedgeFundActivity,
            'tr_InsiderActivity': tr_InsiderActivity, 'tr_TipRanksInvestors': tr_TipRanksInvestors,
            'tr_NewsSentiment': tr_NewsSentiment, 'tr_BloggerOpinions': tr_BloggerOpinions,
            'tr_target_pr': tr_target_pr}


def tipranks_dividends(ticker):
    """
    URL https://www.tipranks.com/api/dividends/getByTicker/?name=INTC&break=1612288126999

    """
    url_tr = f"https://www.tipranks.com/api/dividends/getByTicker/?name={ticker}"
    logger.info(f'-----Tipranks dividends-----')
    logger.info(f'Fetching data for {ticker}')
    logger.debug(f'Using requests on {url_tr}')
    next_ex_dividend_date, dividend_amount, dividend_perc = None, None, None
    ex_date1, ex_date2, ex_date3, ex_date4, ex_date5 = None, None, None, None, None
    try:
        resp = get_page_content(url_tr)
        data = resp.json()
        next_ex_dividend_date = data[0]['exDate']
        dividend_amount = data[0]['amount']
        dividend_perc = data[0]['yield']
        ex_date1 = data[1]['exDate']
        ex_date2 = data[2]['exDate']
        ex_date3 = data[3]['exDate']
        ex_date4 = data[4]['exDate']
        ex_date5 = data[5]['exDate']
    except Exception as exe:
        logger.warning(f'Unable to get data from tipranks_dividends {exe} - {url_tr}')
    return {"tr_next_ex_dividend_date": next_ex_dividend_date, "tr_dividend_amount": dividend_amount,
            "dividend_perc": dividend_perc, "tr_ex_date1": ex_date1, "tr_ex_date2": ex_date2,
            "tr_ex_date3": ex_date3, "tr_ex_date4": ex_date4, "tr_ex_date5": ex_date5}

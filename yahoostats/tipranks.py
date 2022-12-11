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
https://tr-frontend-cdn.azureedge.net/stocks/prod/data/dividend-stocks/payload.json
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

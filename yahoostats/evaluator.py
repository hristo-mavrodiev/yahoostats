#from yahoostats.selenium_stats import Webscraper
from yahoostats.yahoo import yahoo_api_financials
from yahoostats.morningstars import morningstar_stats
from yahoostats.seeking_alpha import seeking_alpha
from yahoostats.zacks import zacks_stats
from yahoostats.reuters import filter_reuters, reuters_stats
from yahoostats.tipranks import tipranks_price, tipranks_analysis, tipranks_dividends
from yahoostats.simplywall import Simplywall

import configparser
from pprint import pprint as pp
from yahoostats.logger import logger
import time
import pandas as pd
import logging
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)

ticker = 'GOOGL'
stock_list = ['GOOGL', 'MU']


def combine_stats(stock_list, browser="Chrome"):
    """
    Merge the data from requests and selenium into pandas df.
    Inputs:
    ------------------
    stocklist - list with stock symbols
    browser = "Chrome" / "Firefox" for default selenium webscraping browser

    Outputs:
    ------------------
    Pandas DataFrame with the webscraped data from:
    -yahoo finance webscraped with selenium - "PEG Ratio"
    -yahoo finance API - all rows with yf prefix
    -tipranks - all rows with prefix tr
    -reuters - all rows with prefix r
    -morningstar -the row with "ms" label represents the star rating 0-5
    -zacks - racks label - represents buy/sell rating
    """
    logger.info(f'Getting data for {stock_list}')
    stock_data = {}
    for stock in stock_list:
        logger.info(f'Evaluator for {stock}')
        stock_data.update({stock: {}})
        yf_rate = yahoo_api_financials(stock)
        ms_rate = morningstar_stats(stock)
        zs_rate = zacks_stats(stock)
        #re_rate = filter_reuters(reuters_stats(stock))
        tr_analys = tipranks_analysis(stock)
        tr_rate = tipranks_price(stock)
        tr_divid = tipranks_dividends(stock)
        sa_rate = seeking_alpha(stock)
        sw_rate = Simplywall(stock.upper()).company_price_rating()

        stock_data[stock].update(tr_analys)
        stock_data[stock].update(tr_rate)
        stock_data[stock].update(tr_divid)
        stock_data[stock].update(sa_rate)

        stock_data[stock].update(yf_rate)
        stock_data[stock].update(ms_rate)
        stock_data[stock].update(zs_rate)
        #stock_data[stock].update(re_rate)
        stock_data[stock].update(sw_rate)
        time.sleep(0.5)

    logger.info(f'Merging data for {stock_list}')
    pd_df = pd.DataFrame(stock_data)
    return pd_df

def future_dividends(df):
    """
    Inputs:
    ------------------
    df - webscraped data

    Outputs:
    ------------------
    Pandas DataFrame with future dividends calendar
    """
    logger.info(f'Cleaning webscraped data for for future dividends')
    df = df.T
    div_data = df[['tr_price','tr_next_ex_dividend_date', 'tr_dividend_amount','r_div_yield5','r_div_yield']]
    div_data['tr_next_ex_dividend_date'] = pd.to_datetime(div_data['tr_next_ex_dividend_date'])
    div_data = div_data.sort_values(by=['tr_next_ex_dividend_date'])
    div_data['tr_dividend_amount'] = div_data['tr_dividend_amount'].str.replace('Currency in US Dollar','$')
    # div_data[div_data['tr_next_ex_dividend_date'] > pd.to_datetime('today')]
    return div_data


if __name__ == "__main__":
    webscraped_data = combine_stats(stock_list)
    pp(webscraped_data)

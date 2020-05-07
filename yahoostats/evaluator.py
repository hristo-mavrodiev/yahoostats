from yahoostats.selenium_stats import Webscraper
from yahoostats.requests_stats import yahoo_api_financials, morningstar_stats
from yahoostats.requests_stats import zacks_stats, filter_reuters, reuters_stats
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
    """
    logger.info(f'Getting data for {stock_list}')
    stock_data = {}
    tr = Webscraper(browser)
    tr.start()
    tr.accept_yf_cockies()
    for stock in stock_list:
        logger.info(f'Evaluator for {stock}')
        stock_data.update({stock: {}})
        yf_rate = yahoo_api_financials(stock)
        ms_rate = morningstar_stats(stock)
        zs_rate = zacks_stats(stock)
        re_rate = filter_reuters(reuters_stats(stock))

        yf_pegr = tr.get_yahoo_statistics(stock)
        tr_analys = tr.tipranks_analysis((stock))
        tr_rate = tr.tipranks_price((stock))
        stock_data[stock].update(tr_analys)
        stock_data[stock].update(tr_rate)
        stock_data[stock].update(yf_pegr)

        stock_data[stock].update(yf_rate)
        stock_data[stock].update(ms_rate)
        stock_data[stock].update(zs_rate)
        stock_data[stock].update(re_rate)
        time.sleep(0.5)
    tr.stop()
    logger.info(f'Merging data for {stock_list}')
    pd_df = pd.DataFrame(stock_data)
    return pd_df


if __name__ == "__main__":
    webscraped_data = combine_stats(stock_list)
    pp(webscraped_data)

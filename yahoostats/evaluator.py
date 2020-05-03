from yahoostats.selenium_stats import Webscraper
from yahoostats.requests_stats import yahoo_api_financials, morningstar_stats
from yahoostats.requests_stats import zacks_stats, filter_reuters, reuters_stats
import configparser
from pprint import pprint as pp
from yahoostats.selenium_stats import FIRE_OPT, PATH_GECKO, YAHOO_URL
import time
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())


ticker = 'GOOGL'
stock_list = ['GOOGL', 'MU']


def combine_stats(stock_list):
    """
    Merge the data from requests and selenium into pandas df.
    """
    stock_data = {}
    tr = Webscraper(YAHOO_URL, PATH_GECKO, FIRE_OPT)
    tr.start()
    for stock in stock_list:
        stock_data.update({stock: {}})
        yf_rate = yahoo_api_financials(stock)
        ms_rate = morningstar_stats(stock)
        zs_rate = zacks_stats(stock)
        re_rate = filter_reuters(reuters_stats(stock))

        tr_analys = tr.tipranks_analysis((stock))
        tr_rate = tr.tipranks_price((stock))
        stock_data[stock].update(tr_analys)
        stock_data[stock].update(tr_rate)

        stock_data[stock].update(yf_rate)
        stock_data[stock].update(ms_rate)
        stock_data[stock].update(zs_rate)
        stock_data[stock].update(re_rate)
        time.sleep(0.5)
    tr.stop()

    pd_df = pd.DataFrame(stock_data)
    return pd_df


if __name__ == "__main__":
    webscraped_data = combine_stats(stock_list)
    pp(webscraped_data)

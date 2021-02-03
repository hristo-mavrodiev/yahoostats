"""
Webscaping with Selenium + Firefox or Chrome.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
logger = logging.getLogger(__name__)


class Webscraper:
    """
    Class for webscraping data from Yahoo finance and Tipranks using Selenium.
    Attributes:
    browser = "Chrome" or "Firefox"
    """
    def __init__(self, browser="Chrome"):
        self._yf_url = f'https://finance.yahoo.com/quote'
        self.browser = browser
        self.__driver = None

    def start(self):
        if self.browser == 'Chrome':
            browser_options = chrome_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument('--no-sandbox')
            self.__driver = webdriver.Chrome(options=browser_options)
        elif self.browser == 'Firefox':
            browser_options = firefox_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument('--no-sandbox')
            self.__driver = webdriver.Firefox(options=browser_options)
        else:
            raise Exception('Please set browser to browser=Firefox or Chrome.')
        logger.info(f'Using {self.browser}')
        time.sleep(1)
        logger.debug('Webdriver Started')

    def accept_yf_cockies(self):
        """Yahoo Finance requires to accept cockies on the fist run."""
        self.__driver.get(self._yf_url)
        try:
            cockie_window = self.__driver.find_element_by_tag_name('body')
            cockie_window.find_element_by_name('agree').click()
            logger.debug('Yahoo Cockies accepted.')
        except Exception as exe:
            logger.warning(f'Unable to accept cockies.{exe}')

    def stop(self):
        try:
            self.__driver.close()
            logger.info('Webscraper has finished.Quit.')
        except Exception as exe:
            logger.warning(f'Unable to stop the Webscraper.{exe}')

    def get_yahoo_statistics(self, ticker):
        stock_data = {}
        logger.info(f'----------Yahoo PEG ratio-----')
        logger.info(f'Yahoo webscraping for  {ticker}')
        stock_url = f"{self._yf_url}/{ticker}/key-statistics?p={ticker}"
        logger.info(f'Yahoo url  {stock_url}')
        try:
            self.__driver.get(stock_url)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            if "Symbols Lookup From Yahoo Finance" in self.__driver.title:
                logger.warning(f'The {ticker} was not found in Yahoo Finance.')
                stock_data.update({"PEG Ratio": '---'})
            else:
                data = soup.find(id="Main")
                tables = data.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    # row_list = list()
                    for tr in rows:
                        td = tr.find_all('td')
                        if len(td) > 1 and td[0].text == 'PEG Ratio (5 yr expected) 1':
                            stock_data.update({td[0].text: td[1].text})
        except Exception as exe:
            logger.warning(f'Unable to get data from Yahoo  {exe}')

        return stock_data


    def estimize_eps(self, ticker):
        """
        https://www.estimize.com/{ticker}/?metric_name=eps&chart=table
        """
        url_ez = f'https://www.estimize.com/{ticker}/?metric_name=eps&chart=table'
        logger.info(f'-----estimize_eps-----')
        logger.info(f'Fetching data for {ticker}')
        logger.debug(f'Using selenium on {url_ez}')
        eps_0, eps_1, eps_2, eps_3 = None, None, None, None
        eps_p1, eps_p2, eps_p3, eps_p4 = None, None, None, None
        try:
            self.__driver.get(url_ez)
            time.sleep(1)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
        except Exception as exe:
            logger.warning(f"Unable to fetch url{url_ez} -{ticker} -{exe}.")
        try:
            wallst_data = soup.find('tbody', {"class": "rel-chart-tbl-group rel-chart-tbl-group-wall-street"}).find_all('tr')[0]
            eps_0 = wallst_data.find_all('td')[-4].text
            eps_1 = wallst_data.find_all('td')[-3].text
            eps_2 = wallst_data.find_all('td')[-2].text
            eps_3 = wallst_data.find_all('td')[-1].text
            eps_p1 = wallst_data.find_all('td')[-5].text
            eps_p2 = wallst_data.find_all('td')[-6].text
            eps_p3 = wallst_data.find_all('td')[-7].text
            eps_p4 = wallst_data.find_all('td')[-8].text
        except Exception as exe:
            logger.warning(f"Unable to get eps{url_ez} -{ticker} -{exe}.")
        return {"eps_-4q": eps_p4, "eps_-3q": eps_p3, "eps_-2q": eps_p2, "eps_-1q": eps_p1,
                "eps_cur": eps_0, "eps_+1q": eps_1, "eps_+2q": eps_2, "eps_+3q": eps_3}

    def scroll(self, px):
        self.__driver.execute_script(f"window.scrollTo(0, {px})")
        logger.debug(f"Scrolled with {px} px")

    def screenshot(self, path):
        self.__driver.save_screenshot(path)
        logger.info(f"Screenshot saved as {path} ")

    def test_run(self):
        try:
            logger.info('Testrun on Selenium')
            self.start()
            self.__driver.get('https://finance.yahoo.com/quote')
            self.stop()
            logger.info('working')
            return True
        except Exception as exe:
            logger.warning(f"Something gone wrong...{exe}")
            return False


def ys_run(ticker, browser="Chrome"):
    yh = Webscraper(browser)
    yh.start()
    yh.accept_yf_cockies()
    result_df = (yh.get_yahoo_statistics(ticker))
    yh.stop()
    return result_df


def tr_run(ticker, browser="Chrome"):
    tr = Webscraper(browser)
    tr.start()
    result_df = tr.tipranks_analysis((ticker))
    result_df.update(tr.tipranks_price((ticker)))
    result_df.update(tr.tipranks_dividend((ticker)))
    tr.stop()
    return result_df

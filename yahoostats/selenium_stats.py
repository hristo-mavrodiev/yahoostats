from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from bs4 import BeautifulSoup
import pandas as pd
import time
import configparser
from pprint import pprint as pp
import logging
logger = logging.getLogger(__name__)

# config = configparser.ConfigParser()
# config.read('config.ini')
# print(config.sections())


class Webscraper:
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
                print(f'The {ticker} was not found in Yahoo Finance.')
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

    def tipranks_analysis(self, ticker):
        """
        https://www.tipranks.com/stocks/amd/stock-analysis
        """
        url_tr = f'https://www.tipranks.com/stocks/{ticker}/stock-analysis'
        logger.info(f'-----Tipranks-----')
        logger.info(f'Fetching data for {ticker}')
        logger.debug(f'Using selenium on {url_tr}')
        data = {}
        try:
            self.__driver.get(url_tr)
            time.sleep(1)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            div_tr_score = soup.find('div', {
                'class': "client-components-ValueChange-shape__Octagon"})
            text_tr_score = div_tr_score.find('tspan').text + "/10"
            data.update({'tr_score': text_tr_score})

            div_boxes = soup.find_all('div', {
                'class': ("client-components-stock-research-smart-score-Factor-"
                          "Factor__Factor")
            })
            for box in div_boxes[:8]:
                k = "tr_" + box.find('header').text
                v = box.find_all('div')[0].find_all('div')[0].text
                data.update({k: v})
        except Exception as exe:
            logger.warning(exe)

        return data

    def tipranks_price(self, ticker):
        """
        Webscrape price prediction for the next 12 months.
        https://www.tipranks.com/stocks/amd/price-target
        http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
        price - target value
        <div class="client-components-stock-research-analysts-price-target-style__actualMoney">

        <div class="client-components-stock-research-analysts-price-target-style__change">
        """

        url_tr = f'https://www.tipranks.com/stocks/{ticker}/price-target'
        logger.info(f'-----tipranks_price-----')
        logger.info(f'Fetching data for {ticker}')
        logger.debug(f'Using selenium on {url_tr}')
        target_pr, target_change = None, None

        try:
            self.__driver.get(url_tr)
            time.sleep(2)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            div_target_pr = soup.find('div', {
                'class': "client-components-stock-research-analysts-price-target-style__actualMoney"})
            target_pr = div_target_pr.find('span')['title']

            div_target_prof = soup.find(
                'div', {"class": "client-components-stock-research-analysts-price-target-style__change"})
            target_change = div_target_prof.find('span').text
        except Exception as exe:
            logger.warning(f"Website changed {exe}")

        return {"tr_target_pr": target_pr, "tr_change": target_change}

    def simplywall(self, ticker):
        """
        https://simplywall.st/stocks/us/media/nasdaq-goog.l/alphabet
        https://simplywall.st/stocks/us/software/nyse-gtt/gtt-communications
        NOT IMPLEMENTED
        """
        url_sw = 'https://simplywall.st/stocks/us'
        return url_sw

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
    tr.stop()
    return result_df


if __name__ == "__main__":
    stock_list = ['GOOGL', 'GTT', 'VMW', 'AMD', 'NVDA', 'TSLA', 'IBM', 'DELL']
    pp(ys_run(stock_list[0]))
    # pp(tr_run('GOOGL'))

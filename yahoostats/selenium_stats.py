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

    def tipranks_dividend(self, ticker):
        """
        Webscrape dividends data if available.
        https://www.tipranks.com/stocks/intc/dividends
        """

        url_tr = f'https://www.tipranks.com/stocks/{ticker}/dividends'
        logger.info(f'-----tipranks_dividends-----')
        logger.info(f'Fetching data for {ticker}')
        logger.debug(f'Using selenium on {url_tr}')
        have_dividend = None
        tr_price, next_ex_dividend_date, dividend_amount, dividend_perc = None, None, None, None
        ex_date1, ex_date2, ex_date3, ex_date4, ex_date5 = None, None, None, None, None

        try:
            self.__driver.get(url_tr)
            time.sleep(2)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
        except Exception as exe:
            logger.warning(f"Unable to fetch url{url} -{ticker} -{exe}.")

        try:    
            have_dividend = soup.find('div', {
                'class': "client-components-StockTabTemplate-NoDataWidget-NoDataWidget__textContainer"})

            if have_dividend == None:
                try:
                    tr_price_div = soup.find('div', {
                        'class':"client-components-stock-bar-stock-bar__priceValue"})
                    tr_price = tr_price_div.find('span').text
                except Exception as exe:
                    logger.warning(f"Unable to fetch tr_price - {ticker} -{exe}.")

                try:
                    div_next_ex_dividend_date = soup.find('div', {
                        'class': "client-components-StockTabTemplate-InfoBox-InfoBox__bodySingleBoxInfo"})
                    next_ex_dividend_date = div_next_ex_dividend_date.text
                except Exception as exe:
                    logger.warning(f"Unable to fetch next_ex_dividend_date - {ticker} -{exe}.")

                try:
                    div_dividend_amount = soup.find_all('div', {
                        "class": "client-components-StockTabTemplate-InfoBox-InfoBox__bodySingleBoxInfo"})[1]
                    dividend_amount = div_dividend_amount.find('span')['title']
                except Exception as exe:
                    logger.warning(f"Unable to fetch next_ex_dividend_date - {ticker} -{exe}.")

                try:
                    div_dividend_perc = soup.find_all('div', {
                        "class": "client-components-StockTabTemplate-InfoBox-InfoBox__bodySingleBoxInfo"})[2]
                    dividend_perc = div_dividend_perc.text
                except Exception as exe:
                    logger.warning(f"Unable to fetch dividend_perc - {ticker} -{exe}.")
                
                ex_date_table = soup.find('div', {"class": "rt-tbody"})
                ex_date1 = ex_date_table.find_all('div', {"class": "rt-tr-group"})[0].find('div').find('div').find('div').text
                ex_date2 = ex_date_table.find_all('div', {"class": "rt-tr-group"})[1].find('div').find('div').find('div').text
                ex_date3 = ex_date_table.find_all('div', {"class": "rt-tr-group"})[2].find('div').find('div').find('div').text
                ex_date4 = ex_date_table.find_all('div', {"class": "rt-tr-group"})[3].find('div').find('div').find('div').text
                ex_date5 = ex_date_table.find_all('div', {"class": "rt-tr-group"})[4].find('div').find('div').find('div').text
        except Exception as exe:
            logger.warning(f"Website changed {exe}")

        return {"tr_price": tr_price, "tr_next_ex_dividend_date": next_ex_dividend_date, "tr_dividend_amount": dividend_amount, 
                "dividend_perc": dividend_perc, "tr_ex_date1": ex_date1, "tr_ex_date2": ex_date2, 
                "tr_ex_date3": ex_date3, "tr_ex_date4": ex_date4, "tr_ex_date5": ex_date5}

    # def simplywall(self, ticker):
    #     """
    #     https://simplywall.st/stocks/us/media/nasdaq-goog.l/alphabet
    #     https://simplywall.st/stocks/us/software/nyse-gtt/gtt-communications
    #     NOT IMPLEMENTED
    #     url_sw = 'https://simplywall.st/stocks/us'
    #     """
    #     pass

    def estimize_eps(self, ticker):
        """
        https://www.estimize.com/{ticker}/?metric_name=eps&chart=table
        """
        url_ez= f'https://www.estimize.com/{ticker}/?metric_name=eps&chart=table'
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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from bs4 import BeautifulSoup
import pandas as pd
import time
import configparser
from pprint import pprint as pp

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())

BROWSER = 'Chrome'
if BROWSER == 'Chrome':
    browser_options = chrome_options()
else:
    browser_options = firefox_options()

browser_options.add_argument("--headless")
browser_options.add_argument('--no-sandbox')
BROWSER_OPT = browser_options
YAHOO_URL = f'https://finance.yahoo.com/quote'


class Webscraper:
    def __init__(self, url, browser_options):
        self._url = url
        self.browser_options = browser_options
        self.__driver = None

    def start(self):
        if BROWSER == 'Chrome':
            self.__driver = webdriver.Chrome(options=self.browser_options)
        else:
            self.__driver = webdriver.Firefox(options=self.browser_options)
        time.sleep(1)
        print('Webdriver Started')

    def accept_cockies(self):
        # cookies = pickle.load(open("cookies.pkl", "rb"))
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
        try:
            self.__driver.get(self._url)
            cockie_window = self.__driver.find_element_by_tag_name('body')
            cockie_window.find_element_by_name('agree').click()
            print('Cockies accepted.')
            # pp(self.__driver.get_cookies())
        except Exception as exe:
            print('Unable to accept cockies.')
            print(exe)

    def stop(self):
        try:
            self.__driver.close()
            print('Webscraper has finished.Quit.')
        except Exception as exe:
            print('Unable to stop the Webscraper.')
            print(exe)

    def get_yahoo_statistics(self, stock_list):
        stock_data = {}
        for stock in stock_list:
            print(f'Start webscraping {stock}')
            stock_url = f"{self._url}/{stock}/key-statistics?p={stock}"
            self.__driver.get(stock_url)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            stock_data.update({stock: {}})
            if "Symbols similar to" in soup.get_text():
                print(f'The stock - {stock} was not found in Yahoo Finance.')
                continue
            else:
                data = soup.find(id="Main")
                tables = data.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    # row_list = list()
                    for tr in rows:
                        td = tr.find_all('td')
                        if len(td) > 1:
                            stock_data[stock].update({td[0].text: td[1].text})

        return stock_data

    def tipranks_analysis(self, ticker):
        """
        https://www.tipranks.com/stocks/amd/stock-analysis
        """
        url_tr = f'https://www.tipranks.com/stocks/{ticker}/stock-analysis'
        self.__driver.get(url_tr)
        time.sleep(1)
        soup = BeautifulSoup(self.__driver.page_source, "html.parser")
        data = {}

        try:
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
            print(exe)

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
        target_pr, target_change = None, None
        self.__driver.get(url_tr)
        time.sleep(2)
        soup = BeautifulSoup(self.__driver.page_source, "html.parser")

        try:
            div_target_pr = soup.find('div', {
                'class': "client-components-stock-research-analysts-price-target-style__actualMoney"})
            target_pr = div_target_pr.find('span')['title']

            div_target_prof = soup.find(
                'div', {"class": "client-components-stock-research-analysts-price-target-style__change"})
            target_change = div_target_prof.find('span').text
        except Exception as exe:
            print(f"Website changed {exe}")

        return {"tr_target_pr": target_pr, "tr_change": target_change}

    def simplywall(self, ticker):
        """
        https://simplywall.st/stocks/us/media/nasdaq-goog.l/alphabet
        https://simplywall.st/stocks/us/software/nyse-gtt/gtt-communications
        """
        pass

    def get_yahoo_list_stocks(self, stock_list):

        result = self.get_yahoo_statistics(stock_list)
        pp(result)
        row_list = list()
        for i in stock_list:
            revenue = result[i].get('Revenue (ttm)')
            peg = result[i].get('PEG Ratio (5 yr expected) 1')
            eps = result[i].get('Diluted EPS (ttm)')
            current_ratio = result[i].get('Current Ratio (mrq)')
            qeg = result[i].get('Quarterly Earnings Growth (yoy)')
            price_book = result[i].get('Price/Book (mrq)')
            oper_cash_flow = result[i].get('Operating Cash Flow (ttm)')
            net_income = result[i].get('Net Income Avi to Common (ttm)')
            beta = result[i].get('Beta (5Y Monthly) ')
            row = [i, revenue, net_income, oper_cash_flow, peg, eps,
                   current_ratio, qeg, price_book, beta]
            row_list.append(row)
        column_list = ['stock', 'revenue', 'net_income', 'oper_cash_flow', 'peg', 'eps',
                       'current_ratio', 'qeg', 'price_book', 'beta']
        df_ys = pd.DataFrame(row_list, columns=column_list)
        return df_ys

    def scroll(self, px):
        self.__driver.execute_script(f"window.scrollTo(0, {px})")
        print(f"Scrolled with {px} px")

    def screenshot(self, path):
        self.__driver.save_screenshot(path)
        print(f"Screenshot saved as {path} ")

    def test_run(self):
        try:
            self.start()
            self.__driver.get('https://finance.yahoo.com/quote')
            self.stop()
            print('working')
            return True
        except Exception as exe:
            print("Something gone wrong...")
            print(exe)
            return False


def ys_run(stock_list):
    yh = Webscraper(YAHOO_URL, BROWSER_OPT)
    yh.start()
    yh.accept_cockies()
    result_df = (yh.get_yahoo_list_stocks(stock_list))
    yh.stop()
    return result_df


def tr_run(ticker):
    tr = Webscraper(YAHOO_URL, BROWSER_OPT)
    tr.start()
    result_df = tr.tipranks_analysis((ticker))
    result_df.update(tr.tipranks_price((ticker)))
    tr.stop()
    return result_df


if __name__ == "__main__":
    stock_list = ['GOOGL', 'GTT', 'VMW', 'AMD', 'NVDA', 'TSLA', 'IBM', 'DELL']
    # ys_run(stock_list)
    pp(tr_run('GOOGL'))

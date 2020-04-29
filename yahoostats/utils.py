from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from pprint import pprint as pp


class Webscraper:
    def __init__(self, url, path_to_geckodriver, firefox_options):
        self._url = url
        self._path_to_geckodriver = path_to_geckodriver
        self.firefox_options = firefox_options
        self.__driver = None

    def start(self):
        self.__driver = webdriver.Firefox(self._path_to_geckodriver, options=self.firefox_options)
        self.__driver.get(self._url)
        time.sleep(1)
        print('Webdriver Started')

    def accept_cockies(self):
        # cookies = pickle.load(open("cookies.pkl", "rb"))
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
        try:
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

    def get_statistics(self, stock_list):
        stock_data = {}
        for stock in stock_list:
            print(f'Start webscraping {stock}')
            stock_url = f"{self._url}/{stock}/key-statistics?p={stock}"
            self.__driver.get(stock_url)
            html = self.__driver.execute_script('return document.body.innerHTML;')
            soup = BeautifulSoup(html, "html.parser")
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

    def scroll(self, px):
        self.__driver.execute_script(f"window.scrollTo(0, {px})")
        print(f"Scrolled with {px} px")

    def screenshot(self, path):
        self.__driver.save_screenshot(path)
        print(f"Screenshot saved as {path} ")

    def test_run(self):
        try:
            browser = webdriver.Firefox(
                self._path_to_geckodriver, options=self.firefox_options)
            browser.get(self._url)
            print('Successful test run')
            browser.close()
            return True
        except Exception as exe:
            print("Something gone wrong...")
            print(exe)
            return False


if __name__ == "__main__":
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument('--no-sandbox')
    url = f'https://finance.yahoo.com/quote'
    path_to_geckodriver = '/usr/local/bin'
    stock_list = ['GOOGL', 'GTT', 'VMW']
    yh = Webscraper(url, path_to_geckodriver, firefox_options)
    yh.start()
    yh.accept_cockies()
    result = yh.get_statistics(stock_list)
    pp(result)
    for i in stock_list:
        peg_stock_0 = result[i].get('PEG Ratio (5 yr expected) 1')
        print(f"PEG Ratio of {i} is {peg_stock_0}")
    yh.stop()

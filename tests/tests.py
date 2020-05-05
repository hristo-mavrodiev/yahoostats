import unittest
from selenium import webdriver
from yahoostats.selenium_stats import Webscraper, ys_run
from yahoostats.selenium_stats import BROWSER_OPT, YAHOO_URL
from yahoostats.evaluator import combine_stats


class TestMethods(unittest.TestCase):
    def test_zero(self):
        print("Sample test to test the testings :)")
        self.assertEqual(":)", ":)")

    def test_selenium(self):
        """
        Test Selenium webdriver is running
        """
        browser = webdriver.Chrome(options=BROWSER_OPT)
        browser.get('http://google.com/')
        title = browser.title
        page_source = browser.page_source
        browser.close()
        self.assertTrue(page_source is not None)
        self.assertEqual(title, 'Google')
        print('Selenium is working.')

    def test_webscrapertestrun(self):
        """
        Test Webscraper class-testrun()
        """
        ys = Webscraper(YAHOO_URL, BROWSER_OPT)
        self.assertTrue(ys.test_run())

    def test_yahoo_list_stats_df(self):
        """
        Test of getting data for list of stocks in df.
        """
        stock_list = ['GOOGL']
        self.assertTrue(ys_run(stock_list) is not None)

    def test_evaluator(self):
        """
        Test of merging requests with selenium data
        """
        stock_list = ['GOOGL', 'MU']
        self.assertTrue(combine_stats(stock_list) is not None)


# if __name__ == '__main__':
#     unittest.main()

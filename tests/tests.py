import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from yahoostats.utils import Webscraper


url = f'https://finance.yahoo.com/quote'
path_to_geckodriver = '/usr/local/bin'
firefox_options = Options()
firefox_options.add_argument("--headless")
firefox_options.add_argument('--no-sandbox')


class TestMethods(unittest.TestCase):
    def test_zero(self):
        print("Sample test to test the testings :)")
        self.assertEqual(":)", ":)")

    def test_selenium(self):
        """
        Test Selenium webdriver is running
        """
        browser = webdriver.Firefox(path_to_geckodriver, options=firefox_options)
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
        ys = Webscraper(url, path_to_geckodriver, firefox_options)
        self.assertTrue(ys.test_run())


# if __name__ == '__main__':
#     unittest.main()

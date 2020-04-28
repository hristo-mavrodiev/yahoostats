import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pickle
from pprint import pprint as pp
from bs4 import BeautifulSoup
import pandas as pd
# from selenium.webdriver.common.keys import Keys


url_test = 'http://thetangle.org'
ticker = 'GOOGL'
url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
path_to_geckodriver = '/usr/local/bin'
firefox_options = Options()
firefox_options.add_argument("--headless")
firefox_options.add_argument('--no-sandbox')


def define_session(url, path_to_geckodriver, firefox_options):
    """
    Fuction to accept the cockies before scraping.
    """

    driver = webdriver.Firefox(path_to_geckodriver, options=firefox_options)
    driver.get(url)
    time.sleep(1)
    cockie_window = driver.find_element_by_tag_name('body')
    cockie_window.find_element_by_name('agree').click()
    # driver.save_screenshot("cockies_accepted.png")
    cockie = driver.get_cookies()
    pickle.dump(cockie, open("cookies.pkl", "wb"))
    print("Cockie saved to cookies.pkl")
    print(str(driver.page_source))
    driver.close()

    return cockie


def webscrape(url, path_to_geckodriver, firefox_options):
    """
    Webscaping the statistics from yahoo.finance with firefox and selenium.
    """

    driver = webdriver.Firefox(path_to_geckodriver, options=firefox_options)
    driver.get(url)
    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    time.sleep(1)
    pelem = driver.find_element_by_tag_name('body')
    pelem.find_element_by_name('agree').click()
    driver.execute_script("window.scrollTo(0, 400)")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find_all('table')[0]
    column_soup = table.find_all('th')
    column_list = []
    for col_name in column_soup:
        column_list.append(col_name.text)
    # print(column_list)
    rows = table.find_all('tr')
    row_list = list()
    for tr in rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if row:
            row_list.append(row)
    # print(row_list)
    if column_list:
        column_list[0] = 'stats'
    df_bs = pd.DataFrame(row_list, columns=column_list)
    df_bs.set_index('stats', inplace=True)
    # driver.save_screenshot("screenshot_yahoo.png")
    # pp(driver.get_cookies())
    driver.close()
    return df_bs


# define_session(url, path_to_geckodriver, firefox_options)
data = webscrape(url, path_to_geckodriver, firefox_options)
print(data)
print(data.columns)
print(data.dtypes)

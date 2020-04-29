"""
Unfortunately this code returns wrong results on the desktop machine.
On colab platform and using google proxy server the results are correct.
Possible issues javascripts are not loaded correctly or need to use cockies.
"""


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as soup
from time import sleep
import pickle
from pprint import pprint as pp
# import locale


proxies = {}
ticker = 'GOOGL'
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
# print(locale.getlocale(0))
# locale.setlocale(locale.LC_ALL, 'en_US.utf8')
# print(locale.getlocale())
# cockie = {'enwiki_session': 'c1bc7dc8-0100-4fac-a608-08a1b6e5f4ed'}
# cookie = pickle.load(open("cookies.pkl", "rb"))


def get_page_content(url):
    s = requests.Session()
    # s.post(url, cockie)
    res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # print(s.cookies.get_dict())
    if res.status_code == requests.codes['ok']:
        soup1 = soup(res.content, "lxml")
        return soup1
    else:
        return None


def yf_stats(ticker, cockie=None, proxies=None,):
    """Function to webscrape stock statistics from yahoo finance.
    ticker: string ticker
    proxies: dictionary with proxy
    """

    # url = "https://finance.yahoo.com/quote/GOOGL/key-statistics?p=GOOGL"
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"
    soup1 = get_page_content(url)
    # print(soup1)
    col = []
    for header in soup1.findAll("th"):
        col.append(header.text)
    print(col)
    try:
        # assert(len(col) == 5)
        df = pd.DataFrame(columns=col)
        for row in soup1.findAll("tr"):
            cells = row.findAll("td")
            row = []
            # print(cells)
            # Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px)
            if len(cells) > 1:
                print(cells[0].text, end='')
                print(" :", cells[1].text)
                # print(" = ", cells[2].find(text=True))
                # print(cells[3].find(text=True), end='')
                # print(cells[4].find(text=True), end='')
                # print(cells[5].find(text=True))
    except Exception as exe:
        print(exe)
        print(f'Wetsite {url} changed need to edit the function.')
        df = pd.DataFrame()
    return df


def reuters_stats(ticker, exchange):
    """
    Function to get data from Thompson Reuters"
    https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&search="COMPANY"
    https://www.reuters.com/companies/GOOGL.O/key-metrics
    """

    url = f"https://www.reuters.com/companies/{ticker}.{exchange}/key-metrics"
    soup1 = get_page_content(url)
    try:
        df = {}
        df.update({ticker: {}})
        for table in soup1.findAll('div', {'class': "KeyMetrics-table-container-3wVZN"}):
            for h3 in table.findAll('h3'):
                print(h3.text)
            for row in table.findAll("tr"):
                keys = row.findAll('th')
                values = row.findAll("td")
                row = []
                if keys and values:
                    print({keys[0].text: values[0].text})
                    df[ticker].update({keys[0].text: values[0].text})
    except Exception as exe:
        print(exe)
        print('Wetsite {url} changed need to edit the function.')
        df = pd.DataFrame()
    return df


# yf_stats(ticker)
pp(reuters_stats(ticker, 'O'))

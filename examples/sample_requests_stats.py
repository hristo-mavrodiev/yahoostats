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


proxies = {}
ticker = 'GOOGL'
# cockie = {'enwiki_session': 'c1bc7dc8-0100-4fac-a608-08a1b6e5f4ed'}
# cookie = pickle.load(open("cookies.pkl", "rb"))


def yf_stats(ticker, cockie, proxies=None,):
    """Function to webscrape stock statistics from yahoo finance.
    ticker: string ticker
    proxies: dictionary with proxy
    """
    s = requests.Session()
    url = "https://finance.yahoo.com/quote/GOOGL/key-statistics?p=GOOGL"
    # post = s.post(url, cockie)
    res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if res.status_code == requests.codes.ok:
        soup1 = soup(res.content, "lxml")
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
                    print(" :", cells[1])
                    # print(" = ", cells[2].find(text=True))
                    # print(cells[3].find(text=True), end='')
                    # print(cells[4].find(text=True), end='')
                    # print(cells[5].find(text=True))
        except Exception as exe:
            print(exe)
            print('Wetsite changed need to edit the function.')
            df = pd.DataFrame()
        return df


yf_stats(ticker, cockie)

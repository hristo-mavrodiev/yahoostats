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
import json
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
"""
Hosts:

    query1.finance.yahoo.com HTTP/1.0
    query2.finance.yahoo.com HTTP/1.1 difference between HTTP/1.0 & HTTP/1.1

If you plan to use a proxy or persistent connections use query2.finance.yahoo.com
But for the purposes of this post the host used for the example URLs is not meant to imply
anything about the path it's being used with.

    We will use HTTP/1.1

Fundamental Data

    /v10/finance/quoteSummary/AAPL?modules= (Full list of modules below)

(substitute your symbol for: AAPL)
Inputs for the ?modules= query:

    modules = [
     'assetProfile',
     'incomeStatementHistory',
     'incomeStatementHistoryQuarterly',
     'balanceSheetHistory',
     'balanceSheetHistoryQuarterly',
     'cashflowStatementHistory',
     'cashflowStatementHistoryQuarterly',
     'defaultKeyStatistics',
     'financialData',
     'calendarEvents',
     'secFilings',
     'recommendationTrend',
     'upgradeDowngradeHistory',
     'institutionOwnership',
     'fundOwnership',
     'majorDirectHolders',
     'majorHoldersBreakdown',
     'insiderTransactions',
     'insiderHolders',
     'netSharePurchaseActivity',
     'earnings',
     'earningsHistory',
     'earningsTrend',
     'industryTrend',
     'indexTrend',
     'sectorTrend' ] #### Example URL:


Querying for: assetProfile and earningsHistory

The %2C is the Hex representation of , and needs to be inserted between each module you
request. details about the hex encoding bit (if you care)
Credits : https://github.com/Gunjan933/stock-market-scraper/blob/master/stock-market-scraper.ipynb

cashflowStatementHistory

current_price = ['currentPrice']
target_price = ['financialData']['targetMeanPrice']
yahoo_ratin = ['financialData']['recommendationMean']
"""


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


def yf_proxy_json(ticker, proxies=None):
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
    html = requests.get(url=url, proxies=proxies).text

    try:
        json_text = html.split('root.App.main =')[1].split(
            '(this)')[0].split(';\n}')[0].strip()

        data = json.loads(json_text)
        result = data["context"]["dispatcher"]["stores"]
        # ['QuoteTimeSeriesStore']
        pp(result)
        return result
    except Exception as exe:
        print(exe)
        print("try another Google's proxy - https://www.proxydocker.com/en/proxylist/platform/google")
        return None


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


def morningstar_stats(ticker):
    """
    https://www.morningstar.com/stocks/xnas/googl/valuation
    https://financials.morningstar.com/ratios/r.html?t=0P0000006A&culture=en&platform=sal
    https://financials.morningstar.com/ratios/r.html?t=GOOGL
    https://financials.morningstar.com/ratios/r.html?t=tsla&culture=en&platform=sal

    <div> class ='r_title'
    <span> id ='star_span'
    """
    pass


def zacks_stats(ticker):
    """
    https://www.zacks.com/stock/chart/GTT/fundamental/peg-ratio-ttm
    https://www.zacks.com/stock/quote/GOOGL/financial-overview
    https://www.zacks.com/stock/quote/TSLA/financial-overview

    <div> class = 'zr_rankbox'
    <p> class = 'rank_view' .text
    """
    url = f'https://www.zacks.com/stock/quote/{ticker}/financial-overview'
    soup_zack = get_page_content(url)
    rating_div = soup_zack.find('div', {'class': 'zr_rankbox'})
    rating_label = rating_div.find('p')
    rating_value = rating_label.text
    print(rating_value.strip())
    return {ticker: rating_value.strip()}


# yf_stats(ticker)
# pp(reuters_stats(ticker, 'O'))
# zacks_stats(ticker)
yf_proxy_json(ticker)

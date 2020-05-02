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
from requests_html import HTMLSession
# import locale


proxies = {}
ticker = 'GOOGL'
stock_list = ['GOOGL', 'GTT', 'VMW', 'AMD', 'NVDA', 'TSLA', 'IBM', 'DELL', 'INTC', 'MU']
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

current_price = ['financialData']['currentPrice']
target_price = ['financialData']['targetMeanPrice']
yahoo_rating = ['financialData']['recommendationMean']

https://yahoo.brand.edgar-online.com/default.aspx?companyid=976409
"""


def get_page_content(url):
    """
    Function to get Beautifulsoup from provided url with requests.
    """
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


def reuters_stats(ticker):
    """
    Function to get data from Thompson Reuters"
    https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&search="COMPANY"
    https://www.reuters.com/companies/GOOGL.O/key-metrics
    https://www.reuters.com/companies/IBM/key-metrics
    O - NASDAQ
    OQ - NASDAQ Stock Exchange Global Select Market
    N - NEWYORK Stock Exchange
    ""or without specified exchange - NEWYORK CONSOLIDATED
    """
    exchanges = ['', '.OQ', '.O', '.N']
    for exchange in exchanges:
        url = f"https://www.reuters.com/companies/{ticker}{exchange}/key-metrics"
        s = requests.Session()
        res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
        used_exchange = ''
        if res.status_code == requests.codes['ok']:
            html = soup(res.text, 'lxml')
            title = html.title.text
            print(title)
            if 'Page Not Found' in title:
                continue
            elif ticker in title:
                soup1 = soup(res.content, "lxml")
                used_exchange = exchange
                break
        soup1 = get_page_content(url)
    try:
        df = {}
        df.update({ticker: {}})
        df[ticker].update({"exchange": used_exchange})
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
        "EPS Growth Rate (5Y)"
        'EPS Growth Rate (3Y)'
        'Dividend Growth Rate (3Y)'
        'Return on Investment (TTM)'
        'Return on Investment (5Y)'
        'Beta'
        'Current Ratio (Annual)'
        'Market Capitalization'
        'EPS Normalized (Annual)'
        'Dividend Yield (5Y)'
        'Dividend Yield'
        'Revenue/Employee (TTM)'
        'Net Income/Employee (TTM)'
        'Net Debt (Annual)'
        'Net Income Available to Common Normalized (Annual)'
    except Exception as exe:
        print(exe)
        print('Wetsite {url} changed need to edit the function.')
        df = pd.DataFrame()
    return df


def morningstar_stats(ticker):
    """
    Function to get stock stars rrating from MorningStar.
    https://www.morningstar.com/stocks/xnas/googl/valuation
    https://financials.morningstar.com/ratios/r.html?t=0P0000006A&culture=en&platform=sal
    https://financials.morningstar.com/ratios/r.html?t=GOOGL
    https://financials.morningstar.com/ratios/r.html?t=tsla&culture=en&platform=sal

    <div> class ='r_title'
    <span> id ='star_span'
    """
    url = f"https://financials.morningstar.com/ratios/r.html?t={ticker}&culture=en&platform=sal"
    soup_ms = get_page_content(url)
    try:
        start_rating = soup_ms.find('span', {'id': "star_span"})
        return {'ms': start_rating["class"][0]}
    except Exception as exe:
        print(exe)
        return None


def zacks_stats(ticker):
    """
    Get Zacks start rating for specific stock.
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
    return {'zacks': rating_value.split()[0]}


def yahoo_api_financials(ticker):
    """
    Get the data from Yahoo API
     Will add later:
    -Revenue
    -Net income
    -Free Cash flow from operations
    -ROE
    -Divident yeld
    -LTG Long-Term Growth (LTG) - https://www.investopedia.com/terms/l/longtermgrowth.asp
    -Return on Assets %
    -Return on Equity %
    """
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=' \
        + 'financialData%2CdefaultKeyStatistics'
    resp = requests.get(url)
    data = resp.json()
    fin_data = data['quoteSummary']['result'][0]['financialData']
    current_price = fin_data['currentPrice'].get('raw')
    target_price = fin_data['targetMeanPrice'].get('raw')
    yahoo_rating_val = fin_data['recommendationMean'].get('raw')
    yahoo_rating_str = fin_data['recommendationKey']
    yahoo_valuation = float(target_price) / float(current_price)
    yahoo_current_ratio = fin_data['currentRatio'].get('raw')
    y_return_assets = fin_data['returnOnAssets'].get('raw') * 100
    y_return_equity = fin_data['returnOnEquity'].get('raw') * 100
    bs_data = data['quoteSummary']['result'][0]['defaultKeyStatistics']
    beta = bs_data['beta'].get('raw')
    result = {'yf_pr_now': current_price,
              'yf_pr_trg': target_price,
              'yf_rv': yahoo_rating_val,
              'yf_rs': yahoo_rating_str,
              'yf_prof': yahoo_valuation,
              'yf_cur_ratio': yahoo_current_ratio,
              'yf_ret_assets': y_return_assets,
              'yf_ret_equity': y_return_equity,
              'yf_beta': beta}
    return result


def combine_stats(ticker_list):
    stock_data = {}
    for stock in stock_list:
        stock_data.update({stock: {}})
        yf_rate = yahoo_api_financials(stock)
        ms_rate = morningstar_stats(stock)
        zs_rate = zacks_stats(stock)
        stock_data[stock].update(yf_rate)
        stock_data[stock].update(ms_rate)
        stock_data[stock].update(zs_rate)

    return stock_data


# yf_stats(ticker)
# pp(reuters_stats(ticker, 'O'))
# print(zacks_stats(ticker))
# pp(yahoo_api_financials(ticker))
# webscraped_data = combine_stats(stock_list)
# pp(webscraped_data)

# yf_proxy_json(ticker)
# morningstar_stats(ticker)
# reuters_stats(ticker)

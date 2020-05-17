yahoostats
==========

[![Python version](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat)](https://pypi.python.org/pypi/yahoostats)
[![Travis-CI build status](https://travis-ci.com/hristo-mavrodiev/yahoostats.svg?token=vBVcih17gwYqyFBxLbq6&branch=master)](https://travis-ci.com/hristo-mavrodiev/yahoostats)
[![CodeFactor](https://www.codefactor.io/repository/github/hristo-mavrodiev/yahoostats/badge?s=4287dd473da0f3410b9a839151234c95fb6c8946)](https://www.codefactor.io/repository/github/hristo-mavrodiev/yahoostats)
[![Codecov](https://codecov.io/gh/hristo-mavrodiev/yahoostats/branch/master/graph/badge.svg?token=XPWG1SQYK5)](https://codecov.io/gh/hristo-mavrodiev/yahoostats)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg?style=flat)](https://pypi.python.org/pypi/yahoostats)
[![PyPi version](https://img.shields.io/pypi/v/yahoostats)](https://pypi.python.org/pypi/yahoostats)
[![PyPi status](https://img.shields.io/pypi/status/yahoostats)](https://pypi.python.org/pypi/yahoostats)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/yahoostats)](https://pypi.python.org/pypi/yahoostats)
[![Docs](https://img.shields.io/badge/Docs-Documentation-green)](https://hristo-mavrodiev.github.io/yahoostats/)
[![Star this repo](https://img.shields.io/github/stars/hristo-mavrodiev/yahoostats)](https://github.com/hristo-mavrodiev/yahoostats)
[![image](https://img.shields.io/badge/Donate-Buy_me_a_coffee-blue.svg)](https://www.buymeacoffee.com/hristomavrodiev)


------------------------------------------------------------------------

***Webscrape stock statistic data from:***
* yahoo finance,
* reuters,
* morningstar,
* zacks.

Quick start
-----------

Try on colab:

[![Python version](https://colab.research.google.com/assets/colab-badge.svg?style=flat)](https://colab.research.google.com/drive/1ISvV7DdK_W_ySwRxSKfDyna6ZsMzQnAb?usp=sharing)

``` {.sourceCode .Python}
from yahoostats.evaluator import combine_stats
stocklist = ['GOOGL', 'TSLA', 'AMD']
combine_stats(stocklist)
```

Explanation for webscraped data:

``` bash
                                        GOOGL
tr_score                                 6/10   Tipranks total score
tr_AnalystRatings                  Strong Buy
tr_BloggerOpinions                    Bullish
tr_Hedge FundActivity               Decreased
tr_InsiderActivity                Sold Shares
tr_TipRanksInvestors                  Neutral
tr_NewsSentiment                      Bullish
tr_Technicals                        Negative
tr_Fundamentals                        17.83%
tr_target_pr                         1482.030    Tipranks target price after 12 months
tr_change                    ▲ (7.06% Upside)    Tipranks
PEG Ratio (5 yr expected) 1              1.94    Yahoo Finance PEG Ratio
yf_pr_now                             1384.34    Yahoo Finance price now
yf_pr_trg                             1515.73    Yahoo Finance target price
yf_rv                                     1.8    Yahoo Finance recomendation score
yf_rs                                     buy    Yahoo Finance recomendation
yf_prof                               1.09491    Yahoo finance profit (target/current price)
yf_cur_ratio                            3.658    Yahoo Finance Current ratio
yf_ret_assets                         0.08712    Yahoo Finance Return on assets
yf_ret_equity                         0.17835    Yahoo Finance Return on equity
yf_beta                                1.0649    Yahoo Finance Beta factor
ms                                    r_star3    Morningstar star rating [0-5]stars
zacks                                  3-Hold    Zacks.com recomentations
r_beta                                   1.06    Reuters Beta factor
r_eps_gr3                               20.82    Reuters EPS_Grow 3 years
r_eps_gr5                               19.92    Reuters EPS Grow 5y
r_div_gr3                                  --    Reuters Dividents grow 3y
r_roi_ttm                               15.56    Reuters Return on investment TTM
r_roi_5                                 15.02    Reuters Return on investment 5years
r_current_ratio                          3.37    Reuters Current ratio
r_mar_cap                          919,046.30    Reuters Market cap
r_net_income                        35,813.79    Reuters Net income
r_net_debt                        -115,121.00    Reuters Net debt
r_div_yield                                --    Reuters dividents yeld
r_div_yield5                               --    Reuters dividents yeld 5 years
r_rev_employee                   1,401,837.00    Reuters Revenue/Employee
r_eps                                   51.27    Reuters Deluted EPS
```


Install system requirements
---------------------------

### On Windows:

  -   Firefox with geckodriver in PATH
  -   Chrome with chrome-driver in PATH

### On Linux:

For Chrome -please check version compatability chrome-driver

``` bash
sudo apt-get update
sudo apt-get install chromium chromium-driver
```

For Firefox -
<https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html>

``` bash
sudo apt-get update
sudo apt-get install wget libgtk-3-0 libdbus-glib-1-2 libxt6

FIREFOX_VERSION=62.0.2 
wget -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2
rm -rf /opt/firefox 
tar -C /opt -xvjf /tmp/firefox.tar.bz2 
rm /tmp/firefox.tar.bz2 
mv /opt/firefox /opt/firefox-$FIREFOX_VERSION 
ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

GECKO_VERSION=0.26.0
wget https://github.com/mozilla/geckodriver/releases/download/v$GECKO_VERSION/geckodriver-v$GECKO_VERSION-linux64.tar.gz  
tar -xvzf geckodriver-v$GECKO_VERSION-linux64.tar.gz   
sudo cp geckodriver /usr/local/bin/
sudo chmod a+x /usr/local/bin/geckodriver
```

Install python requirements on venv
-----------------------------------

### On Windows:

``` bash
python -m venv env
env/Scripts/activate.bat
pip install -r requirements.txt
pip install yahoostats
```

### On Linux:

``` bash
alias python=python3
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install yahoostats
```

Python Requirements
-------------------

-   pandas==1.0.3
-   requests&gt;=2.21.0
-   beautifulsoup4==4.6.3
-   urllib3==1.24.3
-   selenium==3.141.0

License
-------

This project is licensed under the MIT License - see the
[LICENSE.txt](LICENSE.txt)

Acknowledgments
---------------

-   Inspiration
    [ranaroussi/yfinance](https://github.com/ranaroussi/yfinance).
-   Yahoo API docs
    [Gunjan933/stock-market-scraper](https://github.com/Gunjan933/stock-market-scraper).

Donation
--------

If you want to send me a tip:

-   [Buy me a coffee](https://www.buymeacoffee.com/hristomavrodiev)
-   BTC address = 1GfRewxWtovg7gHYiKvGyaxxEhzdN2CMgC
-   LTC address = LS9Jcek1mCrvbpsnbyaCHHtn6iqpM6ef4a


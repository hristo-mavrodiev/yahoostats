yahoostats
============

.. image:: https://img.shields.io/badge/python-3.6+-blue.svg?style=flat
    :target: https://pypi.python.org/pypi/yahoostats
    :alt: Python version

.. image::  https://travis-ci.com/hristo-mavrodiev/yahoostats.svg?token=vBVcih17gwYqyFBxLbq6&branch=master
    :target: https://travis-ci.com/hristo-mavrodiev/yahoostats
    :alt: Travis-CI build status

.. image:: https://www.codefactor.io/repository/github/hristo-mavrodiev/yahoostats/badge?s=4287dd473da0f3410b9a839151234c95fb6c8946
   :target: https://www.codefactor.io/repository/github/hristo-mavrodiev/yahoostats
   :alt: CodeFactor

.. image:: https://codecov.io/gh/hristo-mavrodiev/yahoostats/branch/master/graph/badge.svg?token=XPWG1SQYK5
  :target: https://codecov.io/gh/hristo-mavrodiev/yahoostats
  :alt: Codecov

.. image:: https://img.shields.io/pypi/l/ansicolortags.svg?style=flat
    :target: https://pypi.python.org/pypi/yahoostats
    :alt: PyPI license

.. image:: https://img.shields.io/pypi/v/yahoostats.svg?maxAge=60
    :target: https://pypi.python.org/pypi/yahoostats
    :alt: PyPi version

.. image:: https://img.shields.io/pypi/status/yahoostats.svg?maxAge=60
    :target: https://pypi.python.org/pypi/yahoostats
    :alt: PyPi status

.. image:: https://img.shields.io/pypi/dm/yahoostats.svg?maxAge=2592000&label=installs&color=%2327B1FF
    :target: https://pypi.python.org/pypi/yahoostats
    :alt: PyPi downloads

.. image:: https://img.shields.io/github/stars/hristo-mavrodiev/yahoostats.svg?style=plastic&label=Star&maxAge=60
    :target: https://github.com/hristo-mavrodiev/yahoostats
    :alt: Star this repo


\



=====================================


Webscrape yahoo statistics tab

Install system requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Chrome -please check version compatability chrome-driver

.. code:: bash

    sudo apt-get update
    sudo apt-get install chromium chromium-driver

For Firefox - https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html

.. code:: bash

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


Install python requirements on venv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    alias python=python3
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt


Quick start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://colab.research.google.com/assets/colab-badge.svg?style=flat
    :target: https://colab.research.google.com/drive/1ISvV7DdK_W_ySwRxSKfDyna6ZsMzQnAb?usp=sharing
    :alt: Python version

.. code:: Python

    from yahoostats.evaluator import combine_stats
    stocklist = ['GOOGL', 'TSLA', 'AMD']
    combine_stats(stocklist)

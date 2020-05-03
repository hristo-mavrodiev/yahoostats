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

.. code:: bash

    sudo apt-get update  
    sudo apt-get install firefox wget
    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz  
    tar -xvzf geckodriver-v0.26.0-linux64.tar.gz   
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

.. code:: Python

    from yahoostats.evaluator import combine_stats
    stocklist = ['GOOGL', 'TSLA', 'AMD']
    combine_stats(stocklist)

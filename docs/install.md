# Installation

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

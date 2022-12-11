import requests
from time import sleep
import json
from pprint import pprint as pp
from yahoostats.utils import get_page_content
import logging
logger = logging.getLogger(__name__)
from os import path


HERE = path.abspath(path.dirname(__file__))
HEADERS = {
            'Accept': 'application/json',
            'X-Requested-With': 'sws-services/1.3.7 (Client: browser; SSR: false)',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Content-Type': 'application/json',
          }

class Simplywall:
    """
    Simplywall REST API
    """

    def __init__(self, stock):
        self.stock = stock


    def company_info(self, canonical_url = None):
        """
        URL https://api.simplywall.st/api/company/stocks/us/retail/nasdaq-amzn/amazoncom? \
        include=info%2Cscore%2Cscore.snowflake%2Canalysis.extended.raw_data \
        %2Canalysis.extended.raw_data.insider_transactions&version=2.0 \
        """
        stock = self.stock

        if (stock != None):
            try:
                print("opening")
                db = json.load(open(path.join(HERE, 'simplywall_db.json')))
                print("opening2")
                canonical_url = db[stock]
                print(canonical_url)
            except Exception as exe:
                print(exe)

        url = f"https://api.simplywall.st/api/company{canonical_url}?" \
               "include=info%2Cscore%2Cscore.snowflake%2Canalysis.extended.raw_data" \
               "%2Canalysis.extended.raw_data.insider_transactions&version=2.0"
        print(url)
        response = None
        try:
            response = get_page_content(url)
            response = response.json()
        except Exception as exe:
            pass
        return response


    def company_price_rating(self):
        """
        "Snowflake: value, future, past, health , dividend 1/7"
        """
        price, perc, price_target, score = None, None, None, None
        score_value, score_future, score_past  = None, None, None
        score_health, score_dividend = None, None
        try:
            data = self.company_info()
            price = data['data']['analysis']['data']['share_price']
            perc = data['data']['analysis']['data']['intrinsic_discount']
            price_target = price / (1 - perc / 100)
            #score = data['data']['score']['data']
            snowflake = data['data']['score']['data']['snowflake']['data']['axes']
            score_value = snowflake[0]
            score_future = snowflake[1]
            score_past = snowflake[2]
            score_health = snowflake[3]
            score_dividend = snowflake[4]
        except Exception as exe:
            print(exe)
        return {"sw_price": price, "sw_perc": perc, "sw_price_target": price_target, 
                "sw_score_value": score_value, "sw_score_future": score_future,
                "sw_score_past": score_past, "sw_score_health" : score_health,
                "sw_score_dividend": score_dividend, "sw_score_desc": "score in 1-7"}



if __name__ == "__main__":
    test = Simplywall()
    stock = test.company_price_rating('GOOG')
    pp(stock)

__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import requests

def get_url(url) -> string:
    respsonse = requests.get(url, stream=True)
    return respsonse.content

def get_asx_yield_curve():
    respsonse = get_url("https://www.asx.com.au/content/dam/asx/data/yield_curve.csv")
    return respsonse.content


def get_asx_futures rates():
    respsonse = get_url("https://www.asx.com.au/content/dam/asx/data/market_exp.csv")
    return respsonse.content
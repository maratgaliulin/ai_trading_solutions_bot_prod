import requests
import json

def check_stock_ticker_full(ticker:str):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json?iss.meta=off&iss.only=securities&securities.columns=SECID,LOTSIZE,PREVPRICE"
    try:
        response = json.loads(requests.get(url).text)['securities']['data'][1]
        return response
    except: return [0,0,0]
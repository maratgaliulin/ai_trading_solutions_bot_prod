import requests
import json

def check_stock_ticker(ticker:str):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
    try:
        response = json.loads(requests.get(url).text)['securities']['data'][1][3]
        return response
    except: return None
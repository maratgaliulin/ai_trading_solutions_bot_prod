import requests
import json

def make_currency_list_full():
    url = "https://iss.moex.com/iss/engines/currency/markets/selt/securities.jsonp?iss.meta=off&iss.only=securities&securities.columns=SECID,LOTSIZE,PREVPRICE"
    data = requests.get(url)
    text = json.loads(data.text)['securities']['data']
    currency_list = []
    currency_list_full = []
    for t in text:
        if(
            ((t[0][-7:] == 'RUB_TOM') 
            and
            (len(t[0]) == 10)
            or
            (t[0] == 'USD000UTSTOM')
            or
            (t[0] == 'EUR_RUB__TOM')
            )
            and
            (t[2] != None)            
        ):
            currency_list.append(t[0])
            currency_list_full.append(t)
        
    return currency_list, currency_list_full
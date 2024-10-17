import requests
import json

def make_securities_list():
    url = "https://iss.moex.com/iss/engines/currency/markets/selt/securities.jsonp"
    data = requests.get(url)
    text = json.loads(data.text)['securities']['data']
    currency_list = []
    currency_and_price_list = []
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
            currency_and_price_list.append([t[0], t[14]])
        
    return currency_list, currency_and_price_list
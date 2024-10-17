import requests
import json

def check_bond(isin:str):
    url_corp_all = f"https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off&iss.only=securities&securities.columns=ISIN,SECNAME,BOARDID,LOTSIZE,FACEUNIT,PREVWAPRICE,COUPONVALUE,COUPONPERCENT,COUPONPERIOD,NEXTCOUPON,MATDATE"  
    url_corp_id = f"https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off&iss.only=securities&securities.columns=ISIN"  
    url_federal_all = f"https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQOB/securities.json?iss.meta=off&iss.only=securities&securities.columns=ISIN,SECNAME,BOARDID,LOTSIZE,FACEUNIT,PREVWAPRICE,COUPONVALUE,COUPONPERCENT,COUPONPERIOD,NEXTCOUPON,MATDATE"  
    url_federal_id = f"https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQOB/securities.json?iss.meta=off&iss.only=securities&securities.columns=ISIN"  
    
    response_federal_id_list = json.loads(requests.get(url_federal_id).text)['securities']['data']
    response_corp_id_list = json.loads(requests.get(url_corp_id).text)['securities']['data']

    if ([isin] in response_federal_id_list):
        response_federal_id_all = json.loads(requests.get(url_federal_all).text)['securities']['data']
        response_unit = response_federal_id_all[response_federal_id_list.index([isin])]
        TYPE, ISIN, SECNAME, BOARDID, LOTSIZE, FACEUNIT, PREVWAPRICE, COUPONVALUE, COUPONPERCENT, COUPONPERIOD, NEXTCOUPON, MATDATE = "ОФЗ", response_unit[0], response_unit[1], response_unit[2], response_unit[3], response_unit[4], response_unit[5], response_unit[6], response_unit[7], response_unit[8], response_unit[9], response_unit[10]
        return TYPE, ISIN, SECNAME, BOARDID, LOTSIZE, FACEUNIT, PREVWAPRICE, COUPONVALUE, COUPONPERCENT, COUPONPERIOD, NEXTCOUPON, MATDATE
    
    elif([isin] in response_corp_id_list):
        response_corp_id_all = json.loads(requests.get(url_corp_all).text)['securities']['data']
        response_unit_corp = response_corp_id_all[response_corp_id_list.index([isin])]
        TYPE, ISIN, SECNAME, BOARDID, LOTSIZE, FACEUNIT, PREVWAPRICE, COUPONVALUE, COUPONPERCENT, COUPONPERIOD, NEXTCOUPON, MATDATE = "Корпоративная облигация", response_unit_corp[0], response_unit_corp[1], response_unit_corp[2], response_unit_corp[3], response_unit_corp[4], response_unit_corp[5], response_unit_corp[6], response_unit_corp[7], response_unit_corp[8], response_unit_corp[9], response_unit_corp[10]
        return TYPE, ISIN, SECNAME, BOARDID, LOTSIZE, FACEUNIT, PREVWAPRICE, COUPONVALUE, COUPONPERCENT, COUPONPERIOD, NEXTCOUPON, MATDATE
    else:
        return None
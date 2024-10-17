from methods.components.check_currency_in_the_list import check_currency_in_the_list
from methods.components.make_securities_list import make_securities_list
from methods.components.check_stock_ticker import check_stock_ticker
from methods.components.check_bond import check_bond

def check_currency(ticker:str):
    currency_list, currency_and_price_list = make_securities_list()
    final_ticker_1, final_ticker_2, final_ticker_3 = ticker + 'RUB_TOM', ticker + '_RUB__TOM', ticker + '000UTSTOM'
    stock_price = check_stock_ticker(ticker)
    bond_info = check_bond(ticker)
    
    ticker_1_truefalse, ticker_1_index = check_currency_in_the_list(final_ticker_1, currency_list)
    ticker_2_truefalse, ticker_2_index = check_currency_in_the_list(final_ticker_2, currency_list)
    ticker_3_truefalse, ticker_3_index = check_currency_in_the_list(final_ticker_3, currency_list)

    if(ticker_1_truefalse is True):
        return currency_and_price_list[ticker_1_index][0], currency_and_price_list[ticker_1_index][1]
    elif(ticker_2_truefalse is True):
        return currency_and_price_list[ticker_2_index][0], currency_and_price_list[ticker_2_index][1]
    elif(ticker_3_truefalse is True):
        return currency_and_price_list[ticker_3_index][0], currency_and_price_list[ticker_3_index][1]
    elif(stock_price is not None):
        return ticker, stock_price
    elif(bond_info is not None):
        return bond_info
    else: return None, None
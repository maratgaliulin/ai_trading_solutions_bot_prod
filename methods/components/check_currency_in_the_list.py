def check_currency_in_the_list(input_ticker:str, currency_list:list):
    ticker = input_ticker.upper()
    if (ticker in currency_list):
        return True, currency_list.index(ticker)
    else: return False, -1
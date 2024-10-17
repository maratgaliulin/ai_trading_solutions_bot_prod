from methods.components.check_currency_in_the_list import check_currency_in_the_list
from methods.components.make_securities_list import make_securities_list
from methods.components.check_stock_ticker import check_stock_ticker
from methods.components.save_ticker_to_database import save_ticker_to_database
from methods.components.fetch_ticker_from_database import fetch_ticker
from methods.components.check_bond import check_bond
import sqlite3
from config import *

def save_to_portfolio(portfolio_info:list, user_id:int):
    message_failure = "Что-то пошло не так, данные сохранить не удалось."
    message_error = "Ошибка типа введенных данных."
    
    try:
        ticker = portfolio_info[0].upper()
        purchase_price = float(portfolio_info[1])
        purchase_amount = int(portfolio_info[2])
        currency_list, currency_and_price_list = make_securities_list()
        final_ticker_1, final_ticker_2, final_ticker_3 = ticker + 'RUB_TOM', ticker + '_RUB__TOM', ticker + '000UTSTOM'
        stock_price = check_stock_ticker(ticker)
        bond_info = check_bond(ticker)
        
        ticker_1_truefalse, ticker_1_index = check_currency_in_the_list(final_ticker_1, currency_list)
        ticker_2_truefalse, ticker_2_index = check_currency_in_the_list(final_ticker_2, currency_list)
        ticker_3_truefalse, ticker_3_index = check_currency_in_the_list(final_ticker_3, currency_list)

        if(ticker_1_truefalse is True):
            fetched_ticker = currency_and_price_list[ticker_1_index][0]
            table_name = 'portfolio_currencies'
            msg = save_ticker_to_database(table_name=table_name, 
                    ticker=fetched_ticker, 
                    purchase_price=purchase_price, 
                    purchase_amount=purchase_amount, 
                    user_id=user_id, 
                    db_directory=db_directory)
            return msg
        
        elif(ticker_2_truefalse is True):
            fetched_ticker = currency_and_price_list[ticker_2_index][0]
            table_name = 'portfolio_currencies'
            msg = save_ticker_to_database(table_name=table_name, 
                    ticker=fetched_ticker, 
                    purchase_price=purchase_price, 
                    purchase_amount=purchase_amount, 
                    user_id=user_id, 
                    db_directory=db_directory)
            return msg
                    
        elif(ticker_3_truefalse is True):
            fetched_ticker = currency_and_price_list[ticker_3_index][0]
            table_name = 'portfolio_currencies'
            msg = save_ticker_to_database(table_name=table_name, 
                    ticker=fetched_ticker, 
                    purchase_price=purchase_price, 
                    purchase_amount=purchase_amount, 
                    user_id=user_id, 
                    db_directory=db_directory)
            return msg
        
        elif(stock_price is not None):
            table_name = 'portfolio_shares'
            msg = save_ticker_to_database(table_name=table_name, 
                    ticker=ticker, 
                    purchase_price=purchase_price, 
                    purchase_amount=purchase_amount, 
                    user_id=user_id, 
                    db_directory=db_directory)
            return msg
        
        elif(bond_info is not None):
            table_name = 'portfolio_bonds'
            msg = save_ticker_to_database(table_name=table_name, 
                    ticker=ticker, 
                    purchase_price=purchase_price, 
                    purchase_amount=purchase_amount, 
                    user_id=user_id, 
                    db_directory=db_directory)
            return msg
        
        else: return message_failure

    except: return message_error
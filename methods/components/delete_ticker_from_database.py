from config import *
import sqlite3
from .fetch_ticker_from_database import fetch_ticker

def delete_ticker(table_currencies:str, user_id:int, ticker:str, db_directory:str) -> None:
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_currencies} WHERE user_id = {user_id} AND ticker = '{ticker}'")
    conn.commit()
    conn.close()


def delete_ticker_from_database(ticker:str, user_id:int):
    ticker = ticker.upper()
    table_currencies = 'portfolio_currencies'
    table_shares = 'portfolio_shares'
    table_bonds = 'portfolio_bonds'

    currency_ticker_1, currency_ticker_2, currency_ticker_3 = ticker + 'RUB_TOM', ticker + '_RUB__TOM', ticker + '000UTSTOM'
    
    fetch_currency_ticker_1, fetch_currency_ticker_2, fetch_currency_ticker_3 = fetch_ticker(table_currencies, currency_ticker_1, user_id), fetch_ticker(table_currencies, currency_ticker_2, user_id), fetch_ticker(table_currencies, currency_ticker_3, user_id)
    fetch_stock_ticker = fetch_ticker(table_shares, ticker, user_id)
    fetch_bond_ticker = fetch_ticker(table_bonds, ticker, user_id)

    message_success = 'Данные успешно удалены.'
    message_failure = 'Информация по данному тикеру не найдена в базе данных.'

    if (fetch_currency_ticker_1 is not None):
        delete_ticker(table_currencies, user_id, currency_ticker_1, db_directory)
        return message_success
    elif (fetch_currency_ticker_2 is not None):
        delete_ticker(table_currencies, user_id, currency_ticker_2, db_directory)
        return message_success
    elif (fetch_currency_ticker_3 is not None):
        delete_ticker(table_currencies, user_id, currency_ticker_3, db_directory)
        return message_success
    elif (fetch_stock_ticker is not None):
        delete_ticker(table_shares, user_id, ticker, db_directory)
        return message_success
    elif (fetch_bond_ticker is not None):
        delete_ticker(table_bonds, user_id, ticker, db_directory)
        return message_success    
    else:
        return message_failure
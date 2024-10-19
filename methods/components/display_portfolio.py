from config import *
import sqlite3
import pandas as pd
from datetime import datetime
import math

from .fetch_ruble_position import fetch_ruble_position
from .fetch_user_by_id import fetch_user_by_id
from .fetch_all_tickers_of_a_user import fetch_all_tickers_of_a_user
from .check_stock_ticker_full import check_stock_ticker_full
from .make_currency_list_full import make_currency_list_full
from .check_bond import check_bond

bond_columns = [
                'Тикер',
                'Цена покупки',
                'Количество лотов',
                'Размер лота',
                'Текущая цена',
                'Абс.значение изм.ц.',
                '% изм.цены',
                'Общ.стоим.поз.покуп.',
                'Тек.стоимость поз.',
                '% изм.общей цены',
                'Размер купона',
                'Период купона',
                'Количество оставшихся купонов на акцию',
                'Общее кол-во купонов на позицию',
                ]

stock_and_currency_columns = [
                            'Тикер', 
                            'Цена покупки', 
                            'Текущая цена', 
                            'Количество лотов',
                            'Абс.значение изм.ц.', 
                            '% изм.цены', 
                            'Общ.стоим.поз.покуп.', 
                            'Тек.стоимость поз.', 
                            '% изм.общей цены'
                            ]

def bond_position_info(user_position_info:tuple, ticker_info_from_server:tuple) -> dict:
    now_year = datetime.now().year
    expiration_year = int(ticker_info_from_server[11][0:4])
    years_diff = expiration_year - now_year
    output_dict = {}

    ticker = user_position_info[0]
    purchase_price = round(user_position_info[1] * 10, 2)
    purchase_amount = user_position_info[2]
    lot_size = ticker_info_from_server[4]
    present_price = round(ticker_info_from_server[6] * 10, 2)
    abs_diff = round((present_price - purchase_price),2)
    percent_diff = round((abs_diff / purchase_price * 100), 5)
    total_purchase_value = purchase_price * lot_size * purchase_amount
    total_current_value = present_price * lot_size * purchase_amount
    total_position_value_percent_change = round((total_current_value - total_purchase_value) / total_purchase_value * 100, 2)
    coupon_size = ticker_info_from_server[7]
    coupon_period = ticker_info_from_server[9]
    coupons_left_per_bond = coupon_size * round(365/coupon_period, 0) * years_diff
    coupons_left_per_position = coupons_left_per_bond * purchase_amount

    output_dict[bond_columns[0]] = ticker
    output_dict[bond_columns[1]] = purchase_price
    output_dict[bond_columns[2]] = purchase_amount
    output_dict[bond_columns[3]] = lot_size
    output_dict[bond_columns[4]] = present_price
    output_dict[bond_columns[5]] = abs_diff
    output_dict[bond_columns[6]] = percent_diff
    output_dict[bond_columns[7]] = total_purchase_value
    output_dict[bond_columns[8]] = total_current_value
    output_dict[bond_columns[9]] = total_position_value_percent_change
    output_dict[bond_columns[10]] = coupon_size
    output_dict[bond_columns[11]] = coupon_period
    output_dict[bond_columns[12]] = coupons_left_per_bond
    output_dict[bond_columns[13]] = coupons_left_per_position

    return output_dict

def stock_and_currency_position_info(user_position_info:tuple, ticker_info_from_server:list) -> dict:
    ticker = user_position_info[0]
    purchase_price = user_position_info[1]
    purchase_amount = user_position_info[2]
    lot_size = ticker_info_from_server[1]
    present_price = ticker_info_from_server[2]
    abs_diff = round((present_price - purchase_price),2)
    percent_diff = round((abs_diff / purchase_price * 100), 5)
    total_purchase_value = purchase_price * lot_size * purchase_amount
    total_current_value = present_price * lot_size * purchase_amount
    total_position_value_percent_change = round((total_current_value - total_purchase_value) / total_purchase_value * 100, 2)

    output_dict = {}

    output_dict[stock_and_currency_columns[0]] = ticker
    output_dict[stock_and_currency_columns[1]] = purchase_price
    output_dict[stock_and_currency_columns[2]] = present_price
    output_dict[stock_and_currency_columns[3]] = purchase_amount
    output_dict[stock_and_currency_columns[4]] = abs_diff
    output_dict[stock_and_currency_columns[5]] = percent_diff
    output_dict[stock_and_currency_columns[6]] = total_purchase_value
    output_dict[stock_and_currency_columns[7]] = total_current_value
    output_dict[stock_and_currency_columns[8]] = total_position_value_percent_change

    return output_dict
    

def display_portfolio(user_id:int, db_directory:str) -> str|None:
    db_shares = 'portfolio_shares'
    db_currencies = 'portfolio_currencies'
    db_bonds = 'portfolio_bonds'
    currency_list, currency_list_full = make_currency_list_full()
    total_output = ""
    try:
        rubles = fetch_ruble_position(user_id)
        shares = fetch_all_tickers_of_a_user(db_shares, user_id, db_directory)
        currencies = fetch_all_tickers_of_a_user(db_currencies, user_id, db_directory)
        bonds = fetch_all_tickers_of_a_user(db_bonds, user_id, db_directory)

        shares_list = []
        currencies_list = []
        bonds_list = []

        portfolio_purchase_value = 0.0
        portfolio_current_value = 0.0

        if (rubles is not None):
            portfolio_purchase_value += rubles[0]
            portfolio_current_value += rubles[0]
        
        if(len(shares) > 0):        
            for share in shares:          
                share_info_list = check_stock_ticker_full(share[0])
                share_info_list_item = stock_and_currency_position_info(share, share_info_list)
                shares_list.append(share_info_list_item)
                share_purchase_value = share_info_list_item[stock_and_currency_columns[6]]
                share_current_value = share_info_list_item[stock_and_currency_columns[7]]

                portfolio_purchase_value += share_purchase_value
                portfolio_current_value += share_current_value

        if (len(currencies) > 0):
            for currency in currencies:
                cur_index = currency_list.index(currency[0])
                currency_info_list = currency_list_full[cur_index]
                currency_info_list_item = stock_and_currency_position_info(currency, currency_info_list)
                currencies_list.append(currency_info_list_item)\
                
                currency_purchase_value = currency_info_list_item[stock_and_currency_columns[6]]
                currency_current_value = currency_info_list_item[stock_and_currency_columns[7]]
                portfolio_purchase_value += currency_purchase_value
                portfolio_current_value += currency_current_value


        if (len(bonds) > 0):
            for bond in bonds:
                bond_list_from_server = check_bond(bond[0])
                bond_info_list_item = bond_position_info(bond, bond_list_from_server)
                bonds_list.append(bond_info_list_item)

                bond_purchase_value = bond_info_list_item[bond_columns[7]]
                bond_current_value = bond_info_list_item[bond_columns[8]]
                portfolio_purchase_value += bond_purchase_value
                portfolio_current_value += bond_current_value

        if(len(shares_list) > 0):
            total_output += 'ИНФОРМАЦИЯ ПО АКЦИЯМ\n'
            total_output += '--------------------\n'
            for share in shares_list:
                for key in share.keys():
                    total_output += key + ': ' + str(share[key]) + '\n'
                total_output += '\n'
            total_output += '\n'

        if(len(currencies_list) > 0):
            total_output += 'ИНФОРМАЦИЯ ПО ВАЛЮТАМ\n'
            total_output += '--------------------\n'
            for currency in currencies_list:
                for key in currency.keys():
                    total_output += key + ': ' + str(currency[key]) + '\n'
                total_output += '\n'
            total_output += '\n'

        if(len(bonds_list) > 0):
            total_output += 'ИНФОРМАЦИЯ ПО ОБЛИГАЦИЯМ\n'
            total_output += '--------------------\n'
            for bond in bonds_list:
                for key in bond.keys():
                    total_output += key + ': ' + str(bond[key]) + '\n'
                total_output += '\n'
            total_output += '\n'

        if (
            (portfolio_purchase_value > 0)
            and
            (portfolio_current_value > 0)
        ):        
            portfolio_purchase_abs_difference = round(portfolio_current_value - portfolio_purchase_value, 3)
            portfolio_purchase_percent_difference = round(portfolio_purchase_abs_difference / portfolio_purchase_value * 100, 3)

            total_output += '//////////////////////\n'
            total_output += 'ОБЩАЯ ИНФОРМАЦИЯ ПО ПОРТФЕЛЮ\n'
            total_output += '--------------------\n'

            total_output += f"Изначальная цена портфеля: {portfolio_purchase_value}\n"
            total_output += f"Текущая цена портфеля: {portfolio_current_value}\n"
            total_output += f"Общая прибыль/убыток по портфелю: {portfolio_purchase_abs_difference}\n"
            total_output += f"Процент прибыли/убытка по портфелю: {portfolio_purchase_percent_difference}\n"

        return total_output
    except:
        return None


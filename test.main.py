import sqlite3
import unittest
from unittest import mock
import main as bot
from methods.user.user_class import User
from methods.components.check_currency import check_currency
from methods.components.split_input_info import split_input_info
from methods.components.save_to_portfolio import save_to_portfolio
from methods.components.delete_ticker_from_database import delete_ticker_from_database
from methods.components.check_bond import check_bond
from methods.components.check_currency_in_the_list import check_currency_in_the_list
from methods.components.check_stock_ticker_full import check_stock_ticker_full
from methods.components.make_currency_list_full import make_currency_list_full
from methods.parser.rbc_news_parser import rbc_news_parser
import os


# ПО КАКОЙ-ТО ПРИЧИНЕ У МЕНЯ НЕ ОПРЕДЕЛЯЮТСЯ МЕТОДЫ И КЛАСС USER ПРИ ПОПЫТКЕ ИХ ИМПОРТА ИЗ МЕТОДА MAIN, ПОЭТОМУ ПРИШЛОСЬ ИХ 
# ИМПОРТИРОВАТЬ ФИЗИЧЕСКИ ИЗ СООТВЕТСТВУЮЩИХ ДИРЕКТОРИЙ (СТРОКИ 5-14)


unittest_db_directory = 'database/unittest_database.db'

# Проверка основных методов кода

class UserTestCase(unittest.TestCase):
    unittest_telegram_id = 99999
    username = 'mock_username'
    telegram_nickname = 'mock_user'
    db_directory = unittest_db_directory

    def setUp(self):
        msg_success = "Запись пользователя в БД прошла успешно"
        msg_failure = "Ошибка при записи пользователя в БД"
        try:
            user = User(self.unittest_telegram_id, self.username, self.telegram_nickname, self.db_directory)
            user.write_data()
            result = user.read_data()
            user_tuple = (self.unittest_telegram_id, self.username, self.telegram_nickname)
            test_res = self.assertEqual(result, user_tuple)
            print(test_res)
            print(msg_success)
            return msg_success
        except:
            print(msg_failure)
            return msg_failure
        
    def tearDown(self):
        msg_success = "Удаление пользователя из БД прошло успешно"
        msg_failure = "Ошибка при удалении пользователя из БД"
        try:
            conn = sqlite3.connect(self.db_directory)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM users WHERE telegram_id={self.unittest_telegram_id}")
            conn.commit()            
            conn.close()  
            print(msg_success)          
            return msg_success
        except:
            print(msg_failure)
            return msg_failure
        
    def test_check_user_data(self):
        msg_success = "Тест прошёл успешно"
        msg_failure = "Ошибка при проведении теста"
        user = User(self.unittest_telegram_id, self.username, self.telegram_nickname, self.db_directory)
        result = user.read_data()
        user_tuple = (self.unittest_telegram_id, self.username, self.telegram_nickname)
        equals = self.assertEqual(result, user_tuple)
        if (equals is None):
            print(msg_success)
        else:
            print(msg_failure)

class CheckStockTestCase(unittest.TestCase):

    isin_bond = 'RU000A105G16'
    ticker_share = 'GAZP'
    ticker_currency = 'CNY'
        
    def test_check_ticker(self):
        msg_success = "Тест получения информации по тикеру прошёл успешно"
        msg_failure = "Ошибка при проведении теста получения информации по тикеру"

        try:
            result_bond = check_currency(self.isin_bond)
            result_share = check_currency(self.ticker_share)
            result_currency = check_currency(self.ticker_currency)
            result_incorrect = check_currency('lwenf')

            unittest_bond = self.assertIsNotNone(result_bond[0])
            unittest_share = self.assertIsNotNone(result_share[0])
            unittest_currency = self.assertIsNotNone(result_currency[0])
            unittest_incorrect = self.assertIsNone(result_incorrect[0])
            
            print(msg_success)
            return unittest_bond, unittest_share, unittest_currency, unittest_incorrect
        except:
            print(msg_failure)
            return None

class SavePortfolioTestCase(unittest.TestCase):
    currency_example = "CNY 13.5 35"
    share_example = "AFLT 120 35"
    bond_example = "RU000A106E90 75.0 35"
    incorrect_ticker_example = "sdfns 135 35"
    incorrect_split_example = "AFLT;345;35"

    unittest_telegram_id = 99999
    username = 'mock_username'
    telegram_nickname = 'mock_user'
    db_directory = unittest_db_directory

    user = User(unittest_telegram_id, username, telegram_nickname, db_directory)
    user.write_data()

    def setUp(self):
        msg_success = "Запись актива в БД прошла успешно"
        msg_failure = "Ошибка при записи актива в БД"
        try:
            currency_list = split_input_info(self.currency_example)
            share_list = split_input_info(self.share_example)
            bond_list = split_input_info(self.bond_example)
            incorrect_ticker_list = split_input_info(self.incorrect_ticker_example)
            incorrect_split_list = split_input_info(self.incorrect_split_example)

            currency_message = save_to_portfolio(currency_list, self.unittest_telegram_id)
            share_message = save_to_portfolio(share_list, self.unittest_telegram_id)
            bond_message = save_to_portfolio(bond_list, self.unittest_telegram_id)
            incorrect_data_message = save_to_portfolio(incorrect_ticker_list, self.unittest_telegram_id)
            incorrect_split_message = save_to_portfolio(incorrect_split_list, self.unittest_telegram_id)

            print(currency_message, share_message, bond_message, incorrect_data_message, incorrect_split_message)
            print(msg_success)
            return msg_success
        except:
            print(msg_failure)
            return msg_failure
        
    def tearDown(self):
        msg_success = "Удаление актива из БД прошло успешно"
        msg_failure = "Ошибка при удалении актива из БД"
        try:
            currency_list = split_input_info(self.currency_example)
            share_list = split_input_info(self.share_example)
            bond_list = split_input_info(self.bond_example)

            delete_currency = delete_ticker_from_database(currency_list[0], self.unittest_telegram_id)
            delete_share = delete_ticker_from_database(share_list[0], self.unittest_telegram_id)
            delete_bond = delete_ticker_from_database(bond_list[0], self.unittest_telegram_id)

            print(delete_currency, delete_share, delete_bond)
            return(msg_success)

        except:
            print(msg_failure)
            return msg_failure
        
    def test_check_portfolio_data(self):
        msg_success = "Тест прошёл успешно"
        msg_failure = "Ошибка при проведении теста"
        
        currency_list = split_input_info(self.currency_example)
        share_list = split_input_info(self.share_example)
        bond_list = split_input_info(self.bond_example)
        incorrect_ticker_list = split_input_info(self.incorrect_ticker_example)
        incorrect_split_list = split_input_info(self.incorrect_split_example)

        currency_message = save_to_portfolio(currency_list, self.unittest_telegram_id)
        share_message = save_to_portfolio(share_list, self.unittest_telegram_id)
        bond_message = save_to_portfolio(bond_list, self.unittest_telegram_id)
        incorrect_data_message = save_to_portfolio(incorrect_ticker_list, self.unittest_telegram_id)
        incorrect_split_message = save_to_portfolio(incorrect_split_list, self.unittest_telegram_id)

        print(currency_message, share_message, bond_message, incorrect_data_message, incorrect_split_message)
        print(msg_success)

        self.assertEqual(currency_message, 'Данные успешно изменены.')
        self.assertEqual(share_message, 'Данные успешно изменены.')
        self.assertEqual(bond_message, 'Данные успешно изменены.')
        self.assertEqual(incorrect_data_message, 'Что-то пошло не так, данные сохранить не удалось.')
        self.assertEqual(incorrect_split_message, 'Ошибка типа введенных данных.')

class ParserTestCase(unittest.TestCase):
    db_directory = unittest_db_directory

    def setUp(self):
        rbc_news_parser()
        conn = sqlite3.connect(self.db_directory)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM rbc_news")
        result = cursor.fetchone()
        print('fetch_news_true_false', (result is not None))          
        conn.close()  

    def tearDown(self):
        return super().tearDown() 

    def test_check_news_in_database(self):
        rbc_news_parser()
        conn = sqlite3.connect(self.db_directory)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM rbc_news")
        result = cursor.fetchone()
        print('check_news_in_database_true_false', (result is not None))      
        self.assertIsNotNone(result)
        conn.close()  


# Проверка мелких методов (выбрал отдельные небольшие методы из директории methods.components для тестирования, при необходимости таким же образом можно протестировать все методы)


class CheckBondTestCase(unittest.TestCase):
    bond_example = "RU000A106E90"

    def test_check_bond(self):
        get_bond_info = check_bond(self.bond_example)

        self.assertIsNotNone(get_bond_info)

class CheckCurrencyInTheListTestCase(unittest.TestCase):
    bond_example = "RU000A106E90"
    bond_list_example = ["RU000A101N52", "RU000A1025A7", "RU000A106E90", "RU000A1066D5", "RU000A105B11"]

    def test_check_currency_in_the_list(self):
        bond_in_the_list = check_currency_in_the_list(self.bond_example, self.bond_list_example)

        self.assertTrue(bond_in_the_list[0])

class CheckStockTickerFullTestCase(unittest.TestCase):
    ticker_example = "GAZP"

    def test_check_stock_ticker_full(self):
        stock_ticker_info = check_stock_ticker_full(self.ticker_example)

        self.assertNotEqual(stock_ticker_info, [0,0,0])

class CheckMakeCurrencyListFullMethod(unittest.TestCase):
    currency_example = "CNY"

    def test_make_currency_list_full(self):
        list1, list2 = make_currency_list_full()

        self.assertIn(self.currency_example, list1)



if __name__ == '__main__':
    unittest.main()
import sqlite3
import unittest
from unittest import mock
import main as bot
from methods.user.user_class import User
from methods.components.check_currency import check_currency
import os

unittest_db_directory = 'database/unittest_database.db'


class UserTestCase(unittest.TestCase):
    unittest_telegram_id = 99999
    username = 'mock_username'
    telegram_nickname = 'mock_user'
    db_directory = unittest_db_directory

    def setUp(self):
        msg_success = "Запись пользователя в БД прошло успешно"
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
        try:
            result_bond = check_currency(self.isin_bond)
            result_share = check_currency(self.ticker_share)
            result_currency = check_currency(self.ticker_currency)
            result_incorrect = check_currency('lwenf')

            msg_success = "Тест получения информации по тикеру прошёл успешно"
            msg_failure = "Ошибка при проведении теста получения информации по тикеру"

            unittest_bond = self.assertIsNotNone(result_bond[0])
            unittest_share = self.assertIsNotNone(result_share[0])
            unittest_currency = self.assertIsNotNone(result_currency[0])
            unittest_incorrect = self.assertIsNone(result_incorrect[0])
            
            print(msg_success)
            return unittest_bond, unittest_share, unittest_currency, unittest_incorrect
        except:
            print(msg_failure)
            return None






if __name__ == '__main__':
    unittest.main()
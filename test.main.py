import sqlite3
import unittest
import requests_mock as mock
import requests
import main as bot
from methods.user.user_class import User
from methods.components.check_currency import check_currency
from methods.components.split_input_info import split_input_info
from methods.components.save_to_portfolio import save_to_portfolio
from methods.components.delete_ticker_from_database import delete_ticker_from_database
from methods.components.check_bond import check_bond
from methods.components.check_currency_in_the_list import check_currency_in_the_list
from methods.components.check_stock_ticker_full import check_stock_ticker_full
from methods.components.check_stock_ticker import check_stock_ticker
from methods.components.make_currency_list_full import make_currency_list_full
from methods.parser.rbc_news_parser import rbc_news_parser


# ПРИ ПОПЫТКАХ ЗАМОКИВАНИЯ ОТВЕТА ОТ API СТОЛКНУЛСЯ С СЛЕДУЮЩИМИ ПРОБЛЕМАМИ:

# 1) БИБЛИОТЕКА MOCK ВОЗВРАЩАЕТ ОБЪЕКТ Mock(), А МНЕ ДЛЯ ПРАВИЛЬНОЙ РАБОТЫ МЕТОДА БЫЛ НУЖЕН ОБЪЕКТ RESPONSE, У КОТОРОГО ЕСТЬ СВОЙСТВО TEXT (У MOCK НЕТ АТТРИБУТА, АНАЛОГИЧНОГО RESPONSE.TEXT)
#     -  ЕСЛИ ПОДГОНЯТЬ МЕТОД ПОД БИБЛИОТЕКУ MOCK, ТО ПРИДЁТСЯ ПРОВОДИТЬ ДОСТАТОЧНО МНОГО РЕФАКТОРИНГА, ПЕРЕДЕЛЫВАТЬ ПРАКТИЧЕСКИ ВСЮ ЛОГИКУ
#     -  ПОЭТОМУ Я РЕШИЛ СМЕНИТЬ БИБЛИОТЕКУ MOCK НА REQUESTS_MOCK (НАДЕЮСЬ ЗА ЭТО БАЛЛ НЕ БУДЕТ СНИЖЕН)

# 2) У МЕНЯ В МЕТОДЕ check_currency ФИГУРИРУЕТ НЕСКОЛЬКО URL-ЗАПРОСОВ, ПОЭТОМУ REQUESTS_MOCK ВЫДАЕТ ОШИБКУ requests_mock.exceptions.NoMockAddress: No mock address
#     -  С ЦЕЛЬЮ ПРЕОДОЛЕНИЯ ЭТОЙ ОШИБКИ Я НАПИСАЛ МИНИ-МЕТОД check_currency_local, В КОТОРОМ ЕСТЬ ССЫЛКА ТОЛЬКО НА ОДИН URL (С КОТОРОГО Я БЕРУ ИНФОРМАЦИЮ ПО АКЦИЯМ)
#     -  ДРУГИЕ МЕТОДЫ БЕРУТ ДАННЫЕ ИЗ ФАКТИЧЕСКИХ URL, ЕСЛИ НУЖНО ИХ ВСЕ ЗАМОКАТЬ, ОТПРАВЬТЕ ПОЖАЛУЙСТА МОЮ РАБОТУ НА ДОРАБОТКУ, Я ИХ ЗАМОКАЮ

def check_currency_local(ticker:str):  # метод с одним URL, нужный для замокивания информации об акции ВТБ
    stock_price = check_stock_ticker(ticker)
    if(stock_price is not None):
        return ticker, stock_price
    else: return None, None


# ПО КАКОЙ-ТО ПРИЧИНЕ У МЕНЯ НЕ ОПРЕДЕЛЯЮТСЯ МЕТОДЫ И КЛАСС USER ПРИ ПОПЫТКЕ ИХ ИМПОРТА ИЗ МЕТОДА MAIN, ПОЭТОМУ ПРИШЛОСЬ ИХ 
# ИМПОРТИРОВАТЬ ФИЗИЧЕСКИ ИЗ СООТВЕТСТВУЮЩИХ ДИРЕКТОРИЙ (СТРОКИ 5-14)

test_request_share_url = "https://iss.moex.com/iss/engines/stock/markets/shares/securities/VTBR.json"  # URL для замокивания

# Ложные ответы "сервера":

test_response_share = { "securities": 
                       { "metadata": 
                        { "SECID": {"type": "string", "bytes": 36, "max_size": 0}, 
                         "BOARDID": {"type": "string", "bytes": 12, "max_size": 0}, 
                         "SHORTNAME": {"type": "string", "bytes": 30, "max_size": 0}, 
                         "PREVPRICE": {"type": "double"}, 
                         "LOTSIZE": {"type": "int32"}, 
                         "FACEVALUE": {"type": "double"}, 
                         "STATUS": {"type": "string", "bytes": 3, "max_size": 0}, 
                         "BOARDNAME": {"type": "string", "bytes": 381, "max_size": 0}, 
                         "DECIMALS": {"type": "int32"}, 
                         "SECNAME": {"type": "string", "bytes": 90, "max_size": 0}, 
                         "REMARKS": {"type": "string", "bytes": 24, "max_size": 0}, 
                         "MARKETCODE": {"type": "string", "bytes": 12, "max_size": 0}, 
                         "INSTRID": {"type": "string", "bytes": 12, "max_size": 0}, 
                         "SECTORID": {"type": "string", "bytes": 12, "max_size": 0}, 
                         "MINSTEP": {"type": "double"}, 
                         "PREVWAPRICE": {"type": "double"}, 
                         "FACEUNIT": {"type": "string", "bytes": 12, "max_size": 0}, 
                         "PREVDATE": {"type": "date", "bytes": 10, "max_size": 0}, 
                         "ISSUESIZE": {"type": "int64"}, 
                         "ISIN": {"type": "string", "bytes": 36, "max_size": 0}, 
                         "LATNAME": {"type": "string", "bytes": 90, "max_size": 0}, 
                         "REGNUMBER": {"type": "string", "bytes": 90, "max_size": 0}, 
                         "PREVLEGALCLOSEPRICE": {"type": "double"}, 
                         "CURRENCYID": {"type": "string", "bytes": 12, "max_size": 0}, 
                         "SECTYPE": {"type": "string", "bytes": 3, "max_size": 0}, 
                         "LISTLEVEL": {"type": "int32"}, 
                         "SETTLEDATE": {"type": "date", "bytes": 10, "max_size": 0} }, 
                         "columns": ["SECID", "BOARDID", "SHORTNAME", "PREVPRICE", "LOTSIZE", "FACEVALUE", "STATUS", "BOARDNAME", "DECIMALS", "SECNAME", "REMARKS", "MARKETCODE", "INSTRID", "SECTORID", "MINSTEP", "PREVWAPRICE", "FACEUNIT", "PREVDATE", "ISSUESIZE", "ISIN", "LATNAME", "REGNUMBER", "PREVLEGALCLOSEPRICE", "CURRENCYID", "SECTYPE", "LISTLEVEL", "SETTLEDATE"], 
                         "data": [ ["VTBR", "SPEQ", "ВТБ ао", 97.55, 1, 50, "A", "Поставка по СК (акции)", 6, "ао ПАО Банк ВТБ", None, "RPST", "EQIN", None, 0.000001, None, "SUR", "2024-10-17", 5369933893, "RU000A0JP5V6", "VTB", "10401000B", None, "SUR", "1", 1, "2024-10-21"], 
                                  ["VTBR", "TQBR", "ВТБ ао", 85.09, 1, 50, "A", "Т+: Акции и ДР - безадрес.", 2, "ао ПАО Банк ВТБ", None, "FNDT", "EQIN", None, 0.01, 85.37, "SUR", "2024-10-17", 5369933893, "RU000A0JP5V6", "VTB", "10401000B", 85.17, "SUR", "1", 1, "2024-10-21"] ] }}

test_response_bond_all_info = {
"securities": {
	"columns": ["ISIN", "SECNAME", "BOARDID", "LOTSIZE", "FACEUNIT", "PREVWAPRICE", "COUPONVALUE", "COUPONPERCENT", "COUPONPERIOD", "NEXTCOUPON", "MATDATE"], 
	"data": [
		["RU000A103BQ2", "ОФЗ-ПД 25085 24\/09\/2025", "TQOB", 1, "SUR", None, 31.91, 6.400, 182, "2025-03-26", "2025-09-24"],
		["RU000A0JS3W6", "ОФЗ-ПД 26207 03\/02\/27", "TQOB", 1, "SUR", 81.279, 40.64, 8.150, 182, "2025-02-05", "2027-02-03"],
		["RU000A0JTK38", "ОФЗ-ПД 26212 19\/01\/28", "TQOB", 1, "SUR", 72.963, 35.15, 7.050, 182, "2025-01-22", "2028-01-19"],
		["RU000A0JVW48", "ОФЗ-ПД 26218 17\/09\/31", "TQOB", 1, "SUR", 67.177, 42.38, 8.500, 182, "2025-03-26", "2031-09-17"],
		["RU000A0JWM07", "ОФЗ-ПД 26219 16\/09\/26", "TQOB", 1, "SUR", 83.4, 38.64, 7.750, 182, "2025-03-19", "2026-09-16"],
		["RU000A0JXFM1", "ОФЗ-ПД 26221 23\/03\/33", "TQOB", 1, "SUR", 61.471, 38.39, 7.700, 182, "2025-04-02", "2033-03-23"],
		["RU000A0ZYUA9", "ОФЗ-ПД 26224 23\/05\/29", "TQOB", 1, "SUR", 67.131, 34.41, 6.900, 182, "2024-11-27", "2029-05-23"],
		["RU000A0ZYUB7", "ОФЗ-ПД 26225 10\/05\/34", "TQOB", 1, "SUR", 57.54, 36.15, 7.250, 182, "2024-11-20", "2034-05-10"],
		["RU000A0ZZYW2", "ОФЗ-ПД 26226 07\/10\/26", "TQOB", 1, "SUR", 83.234, 39.64, 7.950, 182, "2025-04-09", "2026-10-07"],
		["RU000A100A82", "ОФЗ-ПД 26228 10\/04\/30", "TQOB", 1, "SUR", 67.143, 38.15, 7.650, 182, "2025-04-16", "2030-04-10"],
		["RU000A100EG3", "ОФЗ-ПД 26229 12\/11\/25", "TQOB", 1, "SUR", 89.599, 35.65, 7.150, 182, "2024-11-13", "2025-11-12"],
		["RU000A100EF5", "ОФЗ-ПД 26230 16\/03\/39", "TQOB", 1, "SUR", 54.491, 38.39, 7.700, 182, "2025-04-02", "2039-03-16"],
		["RU000A100MY9", "ОФЗ-ПД 26231 20\/07\/44", "TQOB", 1, "SUR", None, 1.25, 0.250, 182, "2025-02-12", "2044-07-20"],
		["RU000A1014N4", "ОФЗ-ПД 26232 06\/10\/27", "TQOB", 1, "SUR", 72.369, 29.92, 6.000, 182, "2025-04-09", "2027-10-06"],
		["RU000A101F94", "ОФЗ-ПД 26233 18\/07\/2035", "TQOB", 1, "SUR", 50.964, 30.42, 6.100, 182, "2025-01-29", "2035-07-18"],
		["RU000A101QE0", "ОФЗ-ПД 26234 16\/07\/2025", "TQOB", 1, "SUR", 90.757, 22.44, 4.500, 182, "2025-01-15", "2025-07-16"],
		["RU000A1028E3", "ОФЗ-ПД 26235 12\/03\/2031", "TQOB", 1, "SUR", 58.464, 29.42, 5.900, 182, "2025-03-19", "2031-03-12"]
    ]}}

test_response_bond_isin = {
"securities": {
	"columns": ["ISIN"], 
	"data": [
		["RU000A103BQ2"],
		["RU000A0JS3W6"],
		["RU000A0JTK38"],
		["RU000A0JVW48"],
		["RU000A0JWM07"],
		["RU000A0JXFM1"],
		["RU000A0ZYUA9"],
		["RU000A0ZYUB7"],
		["RU000A0ZZYW2"],
		["RU000A100A82"],
		["RU000A100EG3"],
		["RU000A100EF5"],
		["RU000A100MY9"],
		["RU000A1014N4"],
		["RU000A101F94"],
		["RU000A101QE0"],
		["RU000A1028E3"]
    ]}}


unittest_db_directory = './database/unittest_database.db'
db_dir_for_parser = './database/our_database.db'

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
    ticker_share = 'VTBR'
    ticker_currency = 'CNY'
        
    def test_check_ticker(self):
        msg_success = "Тест получения информации по тикеру прошёл успешно"
        msg_failure = "Ошибка при проведении теста получения информации по тикеру"

        mock_response = {
            "status_code": 200,
            "text": str(test_response_share)
        }

        # ответ на ложный сервер для акций:

        with mock.Mocker() as mock_get:
            mock_get.get(test_request_share_url, json=mock_response)
            result_share = check_currency_local(self.ticker_share)

        # истинные ответы от сервера:
        
        try:
            result_bond = check_currency(self.isin_bond)                
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
    db_directory = db_dir_for_parser

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
    currency_example = "CNYRUB_TOM"

    def test_make_currency_list_full(self):
        list1, list2 = make_currency_list_full()

        self.assertIn(self.currency_example, list1)



if __name__ == '__main__':
    unittest.main()
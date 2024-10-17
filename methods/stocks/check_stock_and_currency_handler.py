from config import *
from methods.components.check_currency import check_currency
from methods.stocks.check_stock_states import CheckTickerStates

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

check_stock_and_currency_router = Router()


@check_stock_and_currency_router.message(Command("check_currency"))
async def check_stock_id(message: types.Message, state:FSMContext):     
    await message.answer("Хотите узнать курс валюты котировку акции или облигации? Введите интересующую вас валюту в формате ХХХ (например: CNY) тикер ценной бумаги (например SBER) или ISIN облигации (например: RU000A0JXQF2):")
    await state.set_state(CheckTickerStates.Ticker)

@check_stock_and_currency_router.message(CheckTickerStates.Ticker)
async def check_stock(message: types.Message, state:FSMContext): 
    await state.update_data(Ticker=message.text)
    data_raw = await state.get_data()
    data = data_raw['Ticker']
    ticker_info = check_currency(data)
    await state.clear()
    if(len(ticker_info) == 2):
        if(ticker_info[0] is not None):
            await message.answer(f"Тикер: {ticker_info[0]}, текущая цена: {ticker_info[1]}") 
    elif(len(ticker_info) > 2):
        await message.answer(f"Информация об облигации: \nТип облигации: {ticker_info[0]} \nISIN: {ticker_info[1]} \nНазвание: {ticker_info[2]} \nИдентификатор типа облигации: {ticker_info[3]} \nРазмер лота: {ticker_info[4]} \nВалюта номинала: {ticker_info[5]} \nЦена: {ticker_info[6]} \nРазмер купона: {ticker_info[7]} \nПроцент купона: {ticker_info[8]} \nПериод купона: {ticker_info[9]} \nДата следующего купона: {ticker_info[10]} \nДата погашения: {ticker_info[11]} \n")
    else:
        await message.answer(f"Тикер {data} не был найден в списке торгуемых валют и ценных бумаг на ПАО Мосбиржа. Попробуйте ввести другой тикер или введите другую команду.")


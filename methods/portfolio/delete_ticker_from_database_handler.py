from config import *
from methods.components.delete_ticker_from_database import delete_ticker_from_database
from .save_portfolio_states import DeleteTickerState

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import sqlite3


delete_ticker_from_database_router = Router()

@delete_ticker_from_database_router.message(Command("delete_ticker"))
async def delete_ticker_start(message: types.Message, state:FSMContext): 
    await message.answer("Хотите удалить информацию о тикере? Введите тикер, который вы бы хотели удалить:")
    await state.set_state(DeleteTickerState.ticker)

@delete_ticker_from_database_router.message(DeleteTickerState.ticker)
async def delete_ticker_finish(message: types.Message, state: FSMContext):
    await state.update_data(ticker=message.text)
    data = await state.get_data()        
    ticker = data['ticker']
    await state.clear()
    if (ticker == 'Да'):    
        msg = delete_ticker_from_database(ticker, message.from_user.id)
        await message.answer(msg)
    else:
        await message.answer("Решили не удалять данный тикер? Хорошо, пока оставим всё как есть.")
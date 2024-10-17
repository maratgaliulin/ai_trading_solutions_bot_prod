from config import *
from methods.components.display_portfolio import display_portfolio

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


display_portfolio_router = Router()

@display_portfolio_router.message(Command("display_portfolio"))
async def display_portfolio_start(message: types.Message, state:FSMContext) -> None:   
    user_id = message.from_user.id
    total_output = display_portfolio(user_id, db_directory)
    if(total_output is None):
        await message.answer(text="Инвестиционные позиции не найдены. Введите информацию о ваших инвестиционных позициях через команду /save_portfolio_element")
    else:
        await message.answer(total_output)
        
from config import *
from methods.components.delete_ruble_position import delete_ruble_position
from methods.components.fetch_ruble_position import fetch_ruble_position

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


delete_ruble_position_router = Router()


@delete_ruble_position_router.message(Command("delete_ruble_position"))
async def delete_ruble_position_start(message: types.Message):    
    await message.answer("Хотите удалить Вашу рублёвую позицию? Введите 'Да' для продолжения.")

@delete_ruble_position_router.message()
async def delete_ruble_position_end(message: types.Message, state:FSMContext): 
    user_id = message.from_user.id
    ruble_position_present = fetch_ruble_position(user_id)
    if(ruble_position_present is None):
        await message.answer("Я не нашел рублевой позиции в моей базе данных.")
    else:
        del_rub_pos = delete_ruble_position(user_id)
        await message.answer(del_rub_pos)
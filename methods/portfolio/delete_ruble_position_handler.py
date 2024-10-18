from config import *
from methods.components.delete_ruble_position import delete_ruble_position
from methods.components.fetch_ruble_position import fetch_ruble_position
from methods.portfolio.delete_ruble_position_state import DeleteRublePositionState

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


delete_ruble_position_router = Router()


@delete_ruble_position_router.message(Command("delete_ruble_position"))
async def delete_ruble_position_start(message: types.Message, state:FSMContext):    
    await state.set_state(DeleteRublePositionState.delete_ruble_position)
    await message.answer("Хотите удалить Вашу рублёвую позицию? Введите 'Да' для продолжения.")

@delete_ruble_position_router.message(DeleteRublePositionState.delete_ruble_position)
async def delete_ruble_position_end(message: types.Message, state:FSMContext): 
    await state.update_data(delete_ruble_position=message.text)
    user_id = message.from_user.id
    ruble_position_present = fetch_ruble_position(user_id)
    data = await state.get_data()
    await state.clear()
    if(data['delete_ruble_position'] == 'Да'):
        if(ruble_position_present is None):
            await message.answer("Я не нашел рублевой позиции в моей базе данных.")
        else:
            delete_ruble_position(user_id)
            await message.answer("Рублевая позиция удалена")
    else:
        await message.answer("Решили не удалять рублёвую позицию? Хорошо, пока оставим всё как есть.")
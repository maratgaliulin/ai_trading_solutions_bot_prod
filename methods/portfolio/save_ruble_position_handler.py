from config import *
from methods.portfolio.save_portfolio_states import SaveRublePosition
from methods.components.save_ruble_position import save_ruble_position
from methods.components.fetch_user_by_id import fetch_user_by_id

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


save_ruble_position_router = Router()


@save_ruble_position_router.message(Command("save_ruble_position"))
async def save_ruble_position_start(message: types.Message, state:FSMContext):    
    await message.answer("Хотите сохранить Вашу рублёвую позицию? Введите величину рублёвой позиции:")
    await state.set_state(SaveRublePosition.ruble_position)

@save_ruble_position_router.message(SaveRublePosition.ruble_position)
async def save_ruble_position_end(message: types.Message, state:FSMContext): 
    user_is_registered = fetch_user_by_id(message.from_user.id)
    if(user_is_registered is None):
        await message.answer("Для отслеживания состояния своего портфеля пользователь должен быть зарегистрирован. Пожалуйста, пройдите регистрацию.")
    else:
        await state.update_data(ruble_position=message.text)
        data_raw = await state.get_data()
        await state.clear()    
        try:        
            data = data_raw['ruble_position']
            data_message = save_ruble_position(message.from_user.id, data, db_directory)
            await message.answer(data_message)
        except: await message.answer("Неверный формат данных. Попробуйте еще раз.")

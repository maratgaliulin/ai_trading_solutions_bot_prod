from config import *
from methods.user.add_user_states import EditUserStates

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import sqlite3

edit_user_router = Router()

@edit_user_router.message(Command("editUsername"))
async def edit_first_name(message: types.Message, state:FSMContext): 
    await state.set_state(EditUserStates.username)
    await message.answer("Хотите исправить Ваше имя? Введите пожалуйста Ваше имя:")

@edit_user_router.message(EditUserStates.username)
async def cmd_edit_first_name(message: types.Message, state:FSMContext): 
    await state.update_data(username=message.text)
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    data = await state.get_data()
    cursor.execute(f"UPDATE users SET username='{data['username']}' WHERE telegram_id={message.from_user.id}")
    user_data = cursor.execute(f'SELECT * FROM users WHERE telegram_id={message.from_user.id}').fetchone()
    conn.commit()
    conn.close()
    await state.clear()
    await message.answer(f"{user_data[1]}, Ваше имя изменено. Введите команду для продолжения моей работы.")
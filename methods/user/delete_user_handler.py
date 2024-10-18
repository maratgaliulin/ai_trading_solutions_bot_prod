from config import *
from methods.components.fetch_user_by_id import fetch_user_by_id
from methods.user.add_user_states import DeleteUserStates

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import sqlite3


delete_user_router = Router()

@delete_user_router.message(Command("delete_user"))
async def delete_user_start(message: types.Message, state: FSMContext): 
    await state.set_state(DeleteUserStates.delete_command)
    await message.answer("Хотите удалить ваши данные? Введите 'Да', чтобы очистить ваши данные.")

@delete_user_router.message(DeleteUserStates.delete_command)
async def delete_user_finish(message: types.Message, state: FSMContext):
    await state.update_data(delete_command=message.text)
    data = await state.get_data()        
    delete_command = data['delete_command']
    await state.clear()
    if (delete_command == 'Да'):
        data = fetch_user_by_id(message.from_user.id)
        if (data is not None):             
            conn = sqlite3.connect(db_directory)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM users WHERE telegram_id={message.from_user.id}")
            cursor.execute(f"DELETE FROM portfolio_bonds WHERE user_id={message.from_user.id}")
            cursor.execute(f"DELETE FROM portfolio_shares WHERE user_id={message.from_user.id}")
            cursor.execute(f"DELETE FROM portfolio_currencies WHERE user_id={message.from_user.id}")
            cursor.execute(f"DELETE FROM ruble_position WHERE client_id={message.from_user.id}")
            conn.commit()
            conn.close()
            await message.answer("Ваши данные успешно удалены. Введите команду для продолжения моей работы.")
        else: 
            await message.answer("Я не нашел вас в моей базе данных. Введите команду для продолжения моей работы.")
    else:
        await message.answer("Введите команду для продолжения моей работы.")
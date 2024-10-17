from config import *
from methods.components.fetch_user_by_id import fetch_user_by_id
from methods.user.user_class import User
from methods.user.add_user_states import AddUserStates

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import os
import sqlite3

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

user_register_router = Router()

@user_register_router.message(Command("start"))
async def cmd_start_and_first_name(message: types.Message, state:FSMContext): 
    result = fetch_user_by_id(message.from_user.id)
    if(result is None):
        await state.set_state(AddUserStates.username)
        photo_file = types.FSInputFile(path=os.path.join(all_media_dir, 'telegram_bot_2.png'))
        msg_id = await message.answer_photo(photo=photo_file, caption="Здравствуйте! Я - финансовый бот-помощник. Назовите пожалуйста Ваше имя.")
        msg_id.photo[0].file_id
    else:
        await message.answer(f"{result[1]}, здравствуйте! Буду рад Вам помочь! Пожалуйста, введите команду для моей работы.")


@user_register_router.message(AddUserStates.username)
async def lets_see(message: types.Message, state:FSMContext): 
    await state.update_data(username=message.text)
    data = await state.get_data()
    await state.clear()
    new_user = User(message.from_user.id, data['username'], message.from_user.username, db_directory)
    new_user_data = new_user.read_data()
    if (new_user_data == None):
        new_user.write_data()
        new_user_data = new_user.read_data()
    await message.answer(f"{new_user_data[1]}, Вы зарегистрированы!")
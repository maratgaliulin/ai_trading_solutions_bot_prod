from config import *
from methods.portfolio.save_portfolio_states import SavePortfolioStates
from methods.components.save_to_portfolio import save_to_portfolio
from methods.components.split_input_info import split_input_info
from methods.components.fetch_user_by_id import fetch_user_by_id

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


save_portfolio_elements_router = Router()


@save_portfolio_elements_router.message(Command("save_portfolio_element"))
async def save_portfolio_element_start(message: types.Message, state:FSMContext):    
    await message.answer("Хотите сохранить Вашу позицию для отслеживания ее статуса? Введите через запятую или пробел: интересующую вас валюту в формате ХХХ, тикер ценной бумаги или ISIN облигации, цену приобретения и количество приобретенных лотов (например RU000A0JXQF2, 95.2, 15):")
    await state.set_state(SavePortfolioStates.portfolio_info)

@save_portfolio_elements_router.message(SavePortfolioStates.portfolio_info)
async def save_portfolio_element_end(message: types.Message, state:FSMContext): 
    user_is_registered = fetch_user_by_id(message.from_user.id)
    if(user_is_registered is None):
        await message.answer("Для отслеживания состояния своего портфеля пользователь должен быть зарегистрирован. Пожалуйста, пройдите регистрацию.")
    else:
        await state.update_data(portfolio_info=message.text)
        data_raw = await state.get_data()
        await state.clear()

        if (data_raw is None):
            await message.answer("К сожалению, я не смог найти информацию с указанным тикером, либо данные были введены неверно.")    
        else:            
            data = data_raw['portfolio_info']
            data_list = split_input_info(data)
            data_message = save_to_portfolio(data_list, message.from_user.id)
            await message.answer(data_message)

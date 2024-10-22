from config import *
import os
from dotenv import load_dotenv
from methods.components.commands import commands
from methods.user.register_user_handler import user_register_router
from methods.user.edit_user_handler import edit_user_router
from methods.user.delete_user_handler import delete_user_router
from methods.stocks.check_stock_and_currency_handler import check_stock_and_currency_router
from methods.portfolio.save_portfolio_elements_handler import save_portfolio_elements_router
from methods.portfolio.save_ruble_position_handler import save_ruble_position_router
from methods.portfolio.delete_ticker_from_database_handler import delete_ticker_from_database_router
from methods.portfolio.delete_ruble_position_handler import delete_ruble_position_router
from methods.portfolio.display_portfolio_handler import display_portfolio_router
from methods.news_scraping.news_scraping_handler import news_scraping_router
from methods.components.menu_button import menu_button
import asyncio
# from methods.anom_vol.anom_vol_handler import anom_vol_handler


import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()

bot_token = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
# bot.set_my_commands(commands=commands)

storage = MemoryStorage()



dp = Dispatcher(storage=storage)


router = Router()

router.include_routers(user_register_router, 
                       edit_user_router, 
                       check_stock_and_currency_router, 
                       save_portfolio_elements_router, 
                       save_ruble_position_router,
                       display_portfolio_router,
                       news_scraping_router,
                       delete_ticker_from_database_router,
                       delete_ruble_position_router,
                       delete_user_router
                       )

dp.include_routers(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await menu_button(bot)
    await dp.start_polling(bot)    

if __name__ == "__main__":     
    asyncio.run(main())
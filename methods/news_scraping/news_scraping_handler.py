from config import *
from .fetch_news_from_database import fetch_news_from_database

import os
from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.enums import ParseMode


news_scraping_router = Router()

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


@news_scraping_router.message(Command("news"))
async def display_news(message: types.Message):   
    all_news = fetch_news_from_database()  
    
    for news in all_news:
        link_to_rbc = f"<a href='{news['link']}'>Полная статья на РБК</a>"
        news_message = f"{news['title'].upper()}\n\n{news['overview']}\n\n\n{link_to_rbc}"
        await message.answer(text=news_message, parse_mode=ParseMode.HTML)
        
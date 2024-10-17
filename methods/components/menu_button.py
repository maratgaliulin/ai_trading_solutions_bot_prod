from methods.components.commands import commands
from aiogram import Bot, Dispatcher, Router
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_default import BotCommandScopeDefault
from aiogram.methods.set_my_commands import SetMyCommands

async def menu_button(dp: Bot):
    await dp.set_my_commands(commands=commands)
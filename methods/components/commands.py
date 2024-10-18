from aiogram.types.bot_command import BotCommand

commands = [
    BotCommand(command="start", description="Нажмите для запуска бота"),
    BotCommand(command="edit_username", description="Редактировать имя пользователя"),
    BotCommand(command="news", description="Список финансовых новостей из РБК"),
    BotCommand(command="check_currency", description="Проверить текущую цену на ценную бумагу или валюту"),
    BotCommand(command="display_portfolio", description="Отобразить информацию об инвестиционном портфеле"),
    BotCommand(command="save_portfolio_element", description="Сохранить информацию о позиции в валюте, ценных бумагах, облигациях"),
    BotCommand(command="save_ruble_position", description="Сохранить рублёвую позицию"),
    BotCommand(command="delete_user", description="Удалить все данные текущего пользователя"),
    BotCommand(command="delete_ticker", description="Удалить информацию о тикере из инвестиционного портфеля"),
    BotCommand(command="delete_ruble_position", description="Удалить рублевую позицию из базы данных")    
]
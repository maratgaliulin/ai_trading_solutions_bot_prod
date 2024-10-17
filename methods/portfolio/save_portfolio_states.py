from aiogram.filters.state import State, StatesGroup

class SavePortfolioStates(StatesGroup):
    portfolio_info = State()

class SaveRublePosition(StatesGroup):
    ruble_position = State()

class DeleteTickerState(StatesGroup):
    ticker = State()
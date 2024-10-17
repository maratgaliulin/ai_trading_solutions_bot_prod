
from aiogram.filters.state import State, StatesGroup

class CheckStockStates(StatesGroup):
    StockID = State()

class CheckTickerStates(StatesGroup):
    Ticker = State()

from aiogram.filters.state import State, StatesGroup

class AddStockStates(StatesGroup):
    StockID = State()
    StockPrice = State()
    StockQuantity = State()
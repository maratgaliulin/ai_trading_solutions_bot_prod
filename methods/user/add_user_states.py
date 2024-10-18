from aiogram.filters.state import State, StatesGroup

class AddUserStates(StatesGroup):
    username = State()

class EditUserStates(StatesGroup):
    username = State()

class DeleteUserStates(StatesGroup):
    delete_command = State()
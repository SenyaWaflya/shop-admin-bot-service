from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    data = State()
    image = State()

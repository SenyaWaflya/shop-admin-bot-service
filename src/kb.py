from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder

add_product = KeyboardButton(text='Добавить товар')
main_kb = ReplyKeyboardBuilder([[add_product]]).as_markup(resize_keyboard=True)

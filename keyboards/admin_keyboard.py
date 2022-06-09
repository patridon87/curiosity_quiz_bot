from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

category_buttons = [
    InlineKeyboardButton(text="Наука и техника", callback_data="Наука и техника"),
    InlineKeyboardButton(
        text="Кино, мультфильмы и ТВ", callback_data="Кино, мультфильмы " "и ТВ"
    ),
    InlineKeyboardButton(text="Литература", callback_data="Литература"),
    InlineKeyboardButton(text="История", callback_data="История"),
    InlineKeyboardButton(text="Искусство", callback_data="Искусство"),
    InlineKeyboardButton(text="Музыка", callback_data="Музыка"),
    InlineKeyboardButton(text="Спорт", callback_data="Спорт"),
    InlineKeyboardButton(text="Игры", callback_data="Игры"),
]


category_keyboard = InlineKeyboardMarkup(row_width=3)
category_keyboard.add(*category_buttons)

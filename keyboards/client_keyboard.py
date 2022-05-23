from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove)

start_game_button = KeyboardButton('/Начнем игру!')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(start_game_button)
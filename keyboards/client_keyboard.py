from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove)

start_game_button = KeyboardButton('/Начнем игру!')
get_question_button = KeyboardButton('/Получить_вопрос')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(start_game_button, get_question_button)
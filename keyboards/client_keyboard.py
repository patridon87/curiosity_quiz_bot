from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

get_question_button = KeyboardButton("/Получить_вопрос")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(get_question_button)

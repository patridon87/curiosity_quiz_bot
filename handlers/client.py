from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client
from database import db


async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'Привет. Это викторина "Curiosity"',
        reply_markup=keyboard_client
    )


async def question(message: types.Message):
    await db.get_question(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(question, commands=['Получить_вопрос'])

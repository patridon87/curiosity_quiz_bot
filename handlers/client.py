from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client


async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'Привет. Это викторина "Curiosity"',
        reply_markup=keyboard_client
    )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
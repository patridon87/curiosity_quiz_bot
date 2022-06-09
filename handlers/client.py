from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import bot
from database import db
from keyboards import keyboard_client


async def command_start(message: types.Message):
    question_count = db.question_count()
    await bot.send_message(
        message.from_user.id,
        f'Привет. Это викторина "Curiosity". Количество '
        f"вопросов в базе -  {question_count[0]}. Чтобы "
        f"получить вопрос нажми кнопку "
        f'"Получить вопрос"',
        reply_markup=keyboard_client,
    )


class FSMClient(StatesGroup):
    question = State()
    check_answer = State()


async def question(message: types.Message, state: FSMContext):
    await FSMClient.question.set()
    async with state.proxy() as data:
        data["question"] = db.get_question()
    if data["question"] is None:
        await state.finish()
        await bot.send_message(message.from_user.id, "Вопросов пока нет")
    else:
        photo = data["question"][1]
        category = data["question"][2]
        text = data["question"][3]
        buttons = [
            InlineKeyboardButton(text=data["question"][4], callback_data=1),
            InlineKeyboardButton(text=data["question"][5], callback_data=2),
            InlineKeyboardButton(text=data["question"][6], callback_data=3),
            InlineKeyboardButton(text=data["question"][7], callback_data=4),
        ]
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        inline_keyboard.add(*buttons)
        if photo == "NULL":
            await bot.send_message(
                message.from_user.id,
                f'Вопрос из категории "{category}":\n ' f"{text}",
                reply_markup=inline_keyboard,
            )
        else:
            await bot.send_photo(
                message.from_user.id,
                photo,
                f'Вопрос из категории "{category}":\n ' f"{text}",
                reply_markup=inline_keyboard,
            )


async def answer_check(callback: types.CallbackQuery, state: FSMContext):
    user_answer = int(callback.data)
    async with state.proxy() as data:
        correct_answer_number = data["question"][8]
    await state.finish()
    if user_answer == correct_answer_number:
        await callback.message.answer("УРА!!! ПРАВИЛЬНЫЙ ОТВЕТ!")
        await callback.answer()
    else:
        correct_answer = data["question"][correct_answer_number + 3]
        await callback.message.answer(f"Правильный ответ:\n"
                                      f"{correct_answer}")
        await callback.answer()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(
        question, commands=["Получить_вопрос"], content_types=["text"],
        state=None
    )
    dp.register_callback_query_handler(
        answer_check, text=[1, 2, 3, 4], state=FSMClient.question
    )

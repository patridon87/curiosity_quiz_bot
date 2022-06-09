import os

from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from database import db
from keyboards.admin_keyboard import category_keyboard

load_dotenv()

ADMIN = int(os.getenv("ADMIN"))


class FSMAdmin(StatesGroup):
    photo = State()
    category = State()
    text = State()
    answer_1 = State()
    answer_2 = State()
    answer_3 = State()
    answer_4 = State()
    correct_answer = State()


async def new_question(message: types.Message):
    if message.from_user.id == ADMIN:
        await FSMAdmin.photo.set()
        await message.reply(
            "Загрузи фото. Если вопрос без фото, отправь "
            "сообщение с любым тектстом"
        )
    else:
        await message.reply("Добавлять вопросы может только администратор")


async def load_photo(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data["photo"] = message.photo[-1].file_id
    else:
        async with state.proxy() as data:
            data["photo"] = "NULL"
    await FSMAdmin.next()
    await message.reply("Выбери категорию вопроса",
                        reply_markup=category_keyboard)


async def enter_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["category"] = callback.data
    await FSMAdmin.next()
    await callback.message.reply("Напиши текст вопроса")
    await callback.answer()


async def enter_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await FSMAdmin.next()
    await message.reply("Напиши вариант ответа №1")


async def enter_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer_1"] = message.text
    await FSMAdmin.next()
    await message.reply("Напиши вариант ответа №2")


async def enter_answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer_2"] = message.text
    await FSMAdmin.next()
    await message.reply("Напиши вариант ответа №3")


async def enter_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer_3"] = message.text
    await FSMAdmin.next()
    await message.reply("Напиши вариант ответа №4")


async def enter_answer_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer_4"] = message.text
        buttons = [
            InlineKeyboardButton(text=data["answer_1"], callback_data=1),
            InlineKeyboardButton(text=data["answer_2"], callback_data=2),
            InlineKeyboardButton(text=data["answer_3"], callback_data=3),
            InlineKeyboardButton(text=data["answer_4"], callback_data=4),
        ]
        correct_answer_keyboard = InlineKeyboardMarkup(
            row_width=2).add(*buttons)
    await FSMAdmin.next()
    await message.reply("Выбери правильный ответ",
                        reply_markup=correct_answer_keyboard)


async def enter_correct_answer(callback: types.CallbackQuery,
                               state: FSMContext):
    async with state.proxy() as data:
        data["correct_answer_number"] = int(callback.data)
    await db.add_question(state)
    await state.finish()
    await callback.message.reply("Вопрос добавлен!")
    await callback.answer()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ввод вопроса отменен")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(new_question, commands="Вопрос", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(
        cancel_handler, Text(equals="отмена", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        load_photo, content_types=["photo", "text"], state=FSMAdmin.photo
    )
    dp.register_callback_query_handler(enter_category, state=FSMAdmin.category)
    dp.register_message_handler(enter_text, content_types=["text"],
                                state=FSMAdmin.text)
    dp.register_message_handler(
        enter_answer_1, content_types=["text"], state=FSMAdmin.answer_1
    )
    dp.register_message_handler(
        enter_answer_2, content_types=["text"], state=FSMAdmin.answer_2
    )
    dp.register_message_handler(
        enter_answer_3, content_types=["text"], state=FSMAdmin.answer_3
    )
    dp.register_message_handler(
        enter_answer_4, content_types=["text"], state=FSMAdmin.answer_4
    )
    dp.register_callback_query_handler(
        enter_correct_answer, text=[1, 2, 3, 4], state=FSMAdmin.correct_answer
    )

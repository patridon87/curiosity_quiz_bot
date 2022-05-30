import os
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from dotenv import load_dotenv
from database import db


load_dotenv()

ADMIN = int(os.getenv('ADMIN'))


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
        await message.reply('Загрузи фото. Если вопрос без фото, отправь '
                            'сообщение с любым тектстом')
    else:
        await message.reply('Добавлять вопросы может только администратор')


async def load_photo(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id
    else:
        async with state.proxy() as data:
            data['photo'] = 'NULL'
    await FSMAdmin.next()
    await message.reply('Выбери категорию вопроса')


async def enter_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMAdmin.next()
    await message.reply('Напиши текст вопроса')


async def enter_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await FSMAdmin.next()
    await message.reply('Напиши вариант ответа №1')


async def enter_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer_1'] = message.text
    await FSMAdmin.next()
    await message.reply('Напиши вариант ответа №2')


async def enter_answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer_2'] = message.text
    await FSMAdmin.next()
    await message.reply('Напиши вариант ответа №3')


async def enter_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer_3'] = message.text
    await FSMAdmin.next()
    await message.reply('Напиши вариант ответа №4')


async def enter_answer_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer_4'] = message.text
    await FSMAdmin.next()
    await message.reply('Напиши номер правильного ответа')


async def enter_correct_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['correct_answer_number'] = message.text
    await db.add_question(state)
    await state.finish()
    await message.reply('Вопрос добавлен!')


async def canсel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ввод вопроса отменен')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(new_question, commands='Вопрос', state=None)
    dp.register_message_handler(canсel_handler, state='*', commands='отмена')
    dp.register_message_handler(canсel_handler,
                                Text(equals='отмена', ignore_case=True),
                                state='*')
    dp.register_message_handler(load_photo, content_types=['photo', 'text'],
                                state=FSMAdmin.photo)
    dp.register_message_handler(enter_category, content_types=['text'],
                                state=FSMAdmin.category)
    dp.register_message_handler(enter_text, content_types=['text'],
                                state=FSMAdmin.text)
    dp.register_message_handler(enter_answer_1, content_types=['text'],
                                state=FSMAdmin.answer_1)
    dp.register_message_handler(enter_answer_2, content_types=['text'],
                                state=FSMAdmin.answer_2)
    dp.register_message_handler(enter_answer_3, content_types=['text'],
                                state=FSMAdmin.answer_3)
    dp.register_message_handler(enter_answer_4, content_types=['text'],
                                state=FSMAdmin.answer_4)
    dp.register_message_handler(enter_correct_answer, content_types=['text'],
                                state=FSMAdmin.correct_answer)

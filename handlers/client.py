from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client
from database import db


async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'Привет. Это викторина "Curiosity"',
        reply_markup=keyboard_client
    )


class FSMClient(StatesGroup):
    question = State()
    check_answer = State()


async def question(message: types.Message, state: FSMContext):
    await FSMClient.question.set()
    async with state.proxy() as data:
        data['question'] = db.get_question()
    if data['question'] is None:
        await state.finish()
        await bot.send_message(message.from_user.id, 'Вопросов пока нет')
    else:
        category = data['question'][2]
        text = data['question'][3]
        answer_1 = data['question'][4]
        answer_2 = data['question'][5]
        answer_3 = data['question'][6]
        answer_4 = data['question'][7]
        await bot.send_message(message.from_user.id,
                               f'Вопрос из категории {category}:\n '
                               f'{text}\n'
                               f'Варианты ответа:\n {answer_1},\n '
                               f'{answer_2},\n {answer_3},\n {answer_4}')


async def answer_check(message: types.Message, state: FSMContext):
    user_answer = message.text
    print(user_answer)
    async with state.proxy() as data:
        correct_answer = data['question'][8]
    await state.finish()
    if user_answer == correct_answer:
        await bot.send_message(message.from_user.id,
                               f'УРА!!! ПРАВИЛЬНЫЙ ОТВЕТ!')
    else:
        await bot.send_message(message.from_user.id, f'Правильный ответ:\n'
                                                     f'{correct_answer}')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(question, commands=['Получить_вопрос'],
                                content_types=['text'],
                                state=None)
    dp.register_message_handler(answer_check, content_types=['text'],
                                state=FSMClient.question)

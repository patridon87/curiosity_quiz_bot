from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import dp
from dotenv import load_dotenv
import os


load_dotenv()

ADMIN = int(os.getenv('ADMIN'))


class FSMAdmin(StatesGroup):
    photo = State()
    theme = State()
    text = State()
    answer_1 = State()
    answer_2 = State()
    answer_3 = State()
    answer_4 = State()
    correct_answer_nubmer = State()


@dp.message_handler(commands='Вопрос', state=None)
async def new_question(message: types.Message):
    if message.from_user.id == ADMIN:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото. Если вопрос без фото, отправь '
                            'сообщение с любым тектстом')
    else:
        await message.reply('Добавлять вопросы может только администратор')


@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    print(message.photo)
    print(message.text)
    if message.photo:
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id
    else:
        async with state.proxy() as data:
            data['photo'] = None
    await FSMAdmin.next()
    await message.reply('ку')

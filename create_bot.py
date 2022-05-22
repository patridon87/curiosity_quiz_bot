from aiogram import Bot
from aiogram.dispatcher import Dispatcher

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN = os.getenv('ADMINS')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

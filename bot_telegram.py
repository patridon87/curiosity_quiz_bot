from aiogram.utils import executor
from create_bot import dp
from handlers import admin, client
from database import db


async def on_startup(_):
    print('Бот онлайн')
    db.sql_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

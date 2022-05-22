from aiogram.utils import executor
from create_bot import dp
from handlers import admin, client


async def on_startup(_):
    print('Бот онлайн')

client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

from aiogram import executor, types
from loader import dp
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from os import getenv
# from sys import exit
# from handlers.menues import start_menu
# from handlers.category_actions import category_handlers_register
# from handlers.product_actions import product_handlers_register
# from handlers.storage_actions import storage_handlers_register
# from handlers.inline_handlers import inline_handlers_register
# from handlers.foundation_actions import foundation_handlers_register
# from handlers.prodarea_actions import prod_area_handlers_register
from handlers import start_menu
from handlers import inline_handlers_register, foundation_handlers_register, prod_area_handlers_register
from handlers import storage_handlers_register, category_handlers_register, product_handlers_register
# from db_tools.user_utils import UserTools
from db_tools import UserTools

# bot_token = getenv("BOT_TOKEN")
# if not bot_token:
#     exit("Error: no token provided")
#
# storage = MemoryStorage()
# bot = Bot(token=bot_token)
# dp = Dispatcher(bot, storage=storage)

inline_handlers_register(dp)
foundation_handlers_register(dp)
prod_area_handlers_register(dp)
storage_handlers_register(dp)
category_handlers_register(dp)
product_handlers_register(dp)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if not await UserTools.get_user(user_id):
        await UserTools.add_user(user_id,
                                 message.from_user.username,
                                 1 if user_id == 681824226 else 2)
    await message.answer(f"Добро пожаловать, {message.from_user.username}")
    await start_menu(message)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

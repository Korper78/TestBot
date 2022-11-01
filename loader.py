from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from sys import exit


bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)

from aiogram import types
# from db_tools import UserTools, FoundTools, ProdAreaTools, StorageTools

# from bot import dp
from db_tools.foundation_utils import FoundTools
from db_tools.prodarea_utils import ProdAreaTools
from db_tools.storage_utils import StorageTools
from keyboards.inline_kb import create_found_kb, create_prod_area_kb, create_storage_kb


# @dp.message_handler(commands="start")
# async def cmd_start(message: types.Message):
#     user_id = message.from_user.id
#     if not await UserTools.get_user(user_id):
#         await UserTools.add_user(user_id,
#                                  message.from_user.username,
#                                  1 if user_id == 681824226 else 2)
#     await message.answer(f"Добро пожаловать, {message.from_user.username}")
#     await start_menu(message)


async def start_menu(message: types.CallbackQuery | types.Message):
    foundations = await FoundTools.get_foundations()
    # print(foundations)
    kb = create_found_kb(foundations)
    if isinstance(message, types.Message):
        await message.answer("Выберите организацию:", reply_markup=kb)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text="Выберите организацию:", reply_markup=kb)
        await call.answer()


async def found_menu(call: types.CallbackQuery | types.Message, foundation_id: int):
    prod_areas = await ProdAreaTools.get_prodareas(foundation_id)
    storages = await StorageTools.get_storages(foundation_id)
    kb = create_prod_area_kb(prod_areas, foundation_id)
    kb2 = create_storage_kb(storages, foundation_id)
    # print(kb.inline_keyboard, kb2.inline_keyboard)
    kb.inline_keyboard.extend(kb2.inline_keyboard)
    # print(kb.inline_keyboard)
    if isinstance(call, types.Message):
        await call.edit_text(text="Выберите производство или склад:", reply_markup=kb)
    else:
        await call.message.edit_text(text="Выберите производство или склад:", reply_markup=kb)
        await call.answer()

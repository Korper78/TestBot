# from bot import dp
from aiogram import types, Dispatcher

from handlers.commands import start_menu, found_menu
from handlers.foundation_actions import create_foundation
from handlers.prodarea_actions import create_prod_area

from keyboards.inline_kb import foundation_cb, prod_area_cb, storage_cb


# @dp.callback_query_handler(foundation_cb.filter())
async def navigate_foundations(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    if choice == 'new':
        await create_foundation(call)
        # await start_menu(call)
    elif choice == 'cancel':
        await start_menu(call)
    else:
        choice = int(choice)
        await found_menu(call, choice)


async def navigate_prod_areas(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    found_id = callback_data.get('found_id')
    if choice == 'new':
        # await CreateProdArea.enter_found_id.set()
        await create_prod_area(call, int(found_id))
        # await start_menu(call)
    elif choice == 'back':
        await start_menu(call)
    else:
        choice = int(choice)
        await prod_area_menu(call, choice)


async def navigate_storages(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    found_id = callback_data.get('found_id')
    if choice == 'new':
        await create_storage(call, int(found_id))
        # await start_menu(call)
    elif choice == 'back':
        await start_menu(call)
    else:
        choice = int(choice)
        await storage_menu(call, choice)


def inline_handlers_register(dp: Dispatcher):
    dp.register_callback_query_handler(navigate_foundations, foundation_cb.filter())
    dp.register_callback_query_handler(navigate_prod_areas, prod_area_cb.filter())
    dp.register_callback_query_handler(navigate_storages, storage_cb.filter())


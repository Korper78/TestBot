# from bot import dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from db_tools.prodarea_utils import ProdAreaTools
from db_tools.storage_utils import StorageTools
from handlers.category_actions import create_category
from handlers.commands import start_menu, found_menu, storage_menu, prod_area_menu
from handlers.foundation_actions import create_foundation
from handlers.prodarea_actions import create_prod_area, prodarea_total, prodarea_produce
from handlers.product_actions import create_product, append_product, ship_product, move_product, move_product_amount, \
    move_product_instance, produce_product
from handlers.storage_actions import create_storage, storage_total, storage_in

from keyboards.inline_kb import foundation_cb, prod_area_cb, storage_cb, store_action_cb, prod_area_action_cb, \
    category_cb, product_cb, prod_action_cb


# @dp.callback_query_handler(foundation_cb.filter())
async def navigate_foundations(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    if choice == 'new':
        await create_foundation(call.message)
    elif choice == 'cancel':
        await call.answer()
        await start_menu(call)
    else:
        choice = int(choice)
        await call.answer()
        await found_menu(call.message, choice)


async def navigate_prod_areas(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    found_id = callback_data.get('found_id')
    if choice == 'new':
        await call.answer()
        await create_prod_area(call, int(found_id))
    # elif choice == 'back':
    #     await start_menu(call)
    else:
        choice = int(choice)
        await call.answer()
        if found_id == '0':
            await move_product_instance(call, choice)
        else:
            await prod_area_menu(call.message, choice)


async def navigate_storages(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    found_id = callback_data.get('found_id')
    if choice == 'new':
        await create_storage(call, int(found_id))
    elif choice == 'back':
        await call.answer()
        await start_menu(call)
    else:
        choice = int(choice)
        # found_id = int(found_id)
        await call.answer()
        if found_id == '0':

            await move_product_instance(call, choice)
        else:
            await storage_menu(call.message, choice)


async def navigate_store_actions(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    store_id = callback_data.get('store_id')
    if choice == 'in':
        await call.answer()
        await storage_in(call.message, int(store_id))
    elif choice == 'out':
        await call.answer()
        await storage_out(call.message, int(store_id))
    elif choice == 'total':
        await call.answer()
        await storage_total(call.message, int(store_id))
    elif choice == 'back':
        storage = await StorageTools.get_storage(store_id)
        choice = storage.foundation_id
        await call.answer()
        await found_menu(call.message, choice)


async def navigate_prodarea_actions(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    prodarea_id = callback_data.get('prod_area_id')
    if choice == 'produce':
        await call.answer()
        await prodarea_produce(call.message, int(prodarea_id))
    elif choice == 'out':
        await call.answer()
        await prodarea_out(call.message, int(prodarea_id))
    elif choice == 'total':
        await call.answer()
        await prodarea_total(call.message, int(prodarea_id))
    elif choice == 'back':
        prodarea = await ProdAreaTools.get_prodarea(prodarea_id)
        choice = prodarea.foundation_id
        await call.answer()
        await found_menu(call.message, choice)


async def navigate_categories(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    place = callback_data.get('place')
    if choice.startswith('new'):
        await call.answer()
        supercategory = int(choice.split('_')[1] or 0)
        await create_category(call, supercategory if supercategory else None, place)
    else:
        # supercategory = int(choice)
        await call.answer()
        place = place.split('_')
        if place[0] == 'storage':
            await storage_in(call.message, int(place[1]), int(choice))
        elif place[0] == 'prodarea':
            await prodarea_produce(call.message, int(place[1]), int(choice))


async def navigate_products(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    place = callback_data.get('place')
    if choice.startswith('new'):
        await call.answer()
        supercategory = int(choice.split('_')[1] or 0)
        await create_product(call, supercategory, place)
    else:
        # supercategory = int(choice)
        await call.answer()
        # place = place.split('_')
        # if place[0] == 'storage':
        if place.startswith('storage'):
            await append_product(call, int(choice), place)
        elif place.startswith('prodarea'):
            await produce_product(call, int(choice), place)


async def navigate_product_actions(call: types.CallbackQuery, callback_data: dict):
    choice = callback_data.get('choice')
    prod_id = int(callback_data.get('prod_id'))
    await call.answer()
    if choice == 'ship':
        await ship_product(call, prod_id)
    else:
        await move_product(call, prod_id)


def inline_handlers_register(dp: Dispatcher):
    dp.register_callback_query_handler(navigate_foundations, foundation_cb.filter())
    dp.register_callback_query_handler(navigate_prod_areas, prod_area_cb.filter(), state='*')
    dp.register_callback_query_handler(navigate_storages, storage_cb.filter(), state='*')
    dp.register_callback_query_handler(navigate_store_actions, store_action_cb.filter())
    dp.register_callback_query_handler(navigate_prodarea_actions, prod_area_action_cb.filter())
    dp.register_callback_query_handler(navigate_categories, category_cb.filter())
    dp.register_callback_query_handler(navigate_products, product_cb.filter(), state='*')
    dp.register_callback_query_handler(navigate_product_actions, prod_action_cb.filter())


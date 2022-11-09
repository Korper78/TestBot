from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from db_tools.category_utils import CategoryTools
# from db_tools.prodarea_utils import ProdAreaTools
# from db_tools.product_utils import ProductTools
from db_tools import ProdAreaTools, CategoryTools, ProductTools
# from handlers.menues import found_menu, prod_area_menu
# from keyboards.inline_kb import make_cb_data, prod_area_cb, create_product_action_kb, foundation_cb, create_product_kb, \
#     create_cat_kb
from keyboards import make_cb_data, prod_area_cb, create_product_action_kb, foundation_cb, create_product_kb, \
    create_cat_kb
from loader import storage


class CreateProdArea(StatesGroup):
    enter_found_id = State()
    enter_name = State()


# async def create_prod_area(call: types.CallbackQuery, found_id: int, state: FSMContext):
# async def create_prod_area(call: types.CallbackQuery, found_id: int):
async def create_prod_area(call: types.CallbackQuery, found_id: int):
    await call.message.edit_text('Введите название производства', reply_markup=None)
    # await call.answer()
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateProdArea.enter_found_id.set()
    await state.update_data(enter_found_id=found_id)
    await CreateProdArea.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_address)
async def enter_prod_area_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['enter_name'] = message.text
    prod_area = await state.get_data()
    print(prod_area)
    res = await ProdAreaTools.add_prodarea(name=prod_area['enter_name'],
                                           foundation_id=prod_area['enter_found_id'])
    print(res)
    await state.finish()
    kb = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Вернуться',
                                   callback_data=make_cb_data(foundation_cb, str(prod_area['enter_found_id']))))
    await message.answer('Принято', reply_markup=kb)
    # await found_menu(message, prod_area['enter_found_id'])


async def prodarea_produce(message: types.Message, prodarea_id: int, supercategory: int = None):
    # store = await StorageTools.get_storage(storage_id)
    if supercategory:
        category = await CategoryTools.get_category(supercategory)
        if category.parent_id:
            super_category = await CategoryTools.get_category(category.parent_id)
            if super_category.parent_id:
                products = await ProductTools.get_products_by_prodarea(prodarea_id)
                products = [(product, await ProductTools.get_product_name(product))
                            for product in products if product.category_id == supercategory]
                kb = create_product_kb(products, 'prodarea_' + str(prodarea_id), supercategory)
                kb.add(InlineKeyboardButton(text='Отменить', callback_data=make_cb_data(prod_area_cb,
                                                                                        str(prodarea_id), ''
                                                                                        # str(store.id),
                                                                                        # str(store.foundation_id)
                                                                                        )))
                # await call.message.edit_text('Выберите товар/материал', reply_markup=kb)
                await message.edit_text('Выберите товар для производства:', reply_markup=kb)
                # if message.text:
                #     await message.edit_text('Выберите товар/материал', reply_markup=kb)
                # else:
                #     await message.answer('Выберите товар/материал', reply_markup=kb)
                # await show_products(message, kb)
            else:
                await show_categories(message, prodarea_id, supercategory)
        else:
            await show_categories(message, prodarea_id, supercategory)
    else:
        await show_categories(message, prodarea_id, supercategory)
    # categories = await CategoryTools.get_categories(supercategory)
    # kb = create_cat_kb(categories, 'storage_' + str(storage_id), supercategory)
    # kb.add(InlineKeyboardButton(text='Отменить', callback_data=make_cb_data(storage_cb,
    #                                                                         str(storage_id), ''
    #                                                                         # str(store.id),
    #                                                                         # str(store.foundation_id)
    #                                                                         )))
    # # await call.message.edit_text('Выберите (под)категорию', reply_markup=kb)
    # await message.edit_text('Выберите (под)категорию:', reply_markup=kb)
    # if message.text:
    #     await message.edit_text('Выберите (под)категорию', reply_markup=kb)
    # else:
    #     await message.answer('Выберите (под)категорию', reply_markup=kb)


async def show_categories(message: types.Message, prodarea_id: int, supercategory: int = None):
    categories = await CategoryTools.get_categories(supercategory)
    kb = create_cat_kb(categories, 'prodarea_' + str(prodarea_id), supercategory)
    kb.add(InlineKeyboardButton(text='Отменить', callback_data=make_cb_data(prod_area_cb,
                                                                            str(prodarea_id), ''
                                                                            # str(store.id),
                                                                            # str(store.foundation_id)
                                                                            )))
    await message.edit_text('Выберите (под)категорию:', reply_markup=kb)


async def prodarea_total(message: types.Message, prodarea_id: int):
    prodarea = await ProdAreaTools.get_prodarea(prodarea_id)
    products = await ProductTools.get_products_by_prodarea(prodarea_id)
    kb = InlineKeyboardMarkup()
    # names = ProductTools.get_product_names()
    for product in products:
        category = await CategoryTools.get_category(product.category_id)
        name = await ProductTools.get_product_name(product)
        prod_kb = create_product_action_kb(product.id, name, category.name, product.amount)
        kb.inline_keyboard.extend(prod_kb.inline_keyboard)
        # await message.answer(f'{name} в категории {category.name}, в количестве {product.amount}',
        #                      reply_markup=kb)
    kb.add(InlineKeyboardButton(text='Назад',
                                callback_data=make_cb_data(prod_area_cb,
                                                           str(prodarea_id), ''
                                                           )))
    await message.edit_text(f'На производстве "{prodarea.name}" имеются следующие материалы/товары:',
                            reply_markup=kb)


def prod_area_handlers_register(dp: Dispatcher):
    # dp.register_message_handler(create_prod_area, state=CreateProdArea.enter_found_id)
    dp.register_message_handler(enter_prod_area_name, state=CreateProdArea.enter_name)

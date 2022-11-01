from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_tools.category_utils import CategoryTools
from db_tools.prodarea_utils import ProdAreaTools
from db_tools.product_utils import ProductTools
from handlers.commands import found_menu, prod_area_menu
from keyboards.inline_kb import make_cb_data, prod_area_cb, create_product_action_kb
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
    await found_menu(message, prod_area['enter_found_id'])


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

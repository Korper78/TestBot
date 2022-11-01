from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))
from db_tools.product_utils import ProductTools
from handlers.storage_actions import storage_in
from keyboards.inline_kb import make_cb_data, category_cb
from loader import storage, bot


class CreateProduct(StatesGroup):
    # enter_place = State()
    # enter_category = State()
    enter_ids = State()
    enter_name = State()
    enter_amount = State()
    append_amount = State()
    change_amount = State()


# async def show_products(message: types.Message, kb: types.InlineKeyboardMarkup):
#     await message.edit_text('Выберите товар/материал:', reply_markup=kb)

# async def create_foundation(call: types.CallbackQuery, state: FSMContext = '*'):
# async def create_product(call: types.CallbackQuery, supercategory: int, place: str):
async def create_product(call: types.CallbackQuery, supercategory: int, place: str):
    # await state.set_state(CreateFoundation.enter_name)
    # await call.answer()
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateProduct.enter_ids.set()
    _place = place.split('_')
    if _place[0] == 'storage':
        storage_id = int(_place[1])
        prodarea_id = None
        products = await ProductTools.get_products_by_storage(storage_id)
    else:
        storage_id = None
        prodarea_id = int(_place[1])
        products = await ProductTools.get_products_by_prodarea(prodarea_id)
    ids = {'category_id': supercategory,
           'storage_id': storage_id,
           'production_area_id': prodarea_id,
           'place': place}
    await state.update_data(enter_ids=ids)
    print(await state.get_data())
    # names = await ProductTools.get_product_names()
    await call.message.edit_text('Введите название материала/товара', reply_markup=None)
    names = [await ProductTools.get_product_name(product)
             for product in products if product.category_id == supercategory]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # kb.add([types.KeyboardButton(text=name.name) for name in names])
    # kb.add([types.KeyboardButton(text=name) for name in names])
    kb.add(names)
    if names:
        await call.message.answer('или выберите из имеющихся:', reply_markup=kb)
    # await message.answer('Введите или выберите название материала/товара', reply_markup=kb)
    await CreateProduct.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_name)
async def enter_product_name(message: types.Message, state: FSMContext):
    name = message.text
    name_id = await ProductTools.add_product_name(name)
    if name_id:
        async with state.proxy() as data:
            data['enter_name'] = name_id
        await message.answer('Введите количество:', reply_markup=types.ReplyKeyboardRemove())
        await CreateProduct.enter_amount.set()
    else:
        await message.answer('Такое название уже есть в другой категории. Повторите ввод:')
        await CreateProduct.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_address)
async def enter_product_amount(message: types.Message, state: FSMContext):
    # await message.edit_text('Введите адрес организации', reply_markup=None)
    amount = message.text
    try:
        async with state.proxy() as data:
            data['enter_amount'] = int(amount)
        product = await state.get_data()
        print(product)
        res = await ProductTools.add_product(amount=product['enter_amount'],
                                             material_id=product['enter_name'],
                                             category_id=product['enter_ids']['category_id'],
                                             storage_id=product['enter_ids']['storage_id'],
                                             production_area_id=product['enter_ids']['production_area_id'],
                                             )
        print(res)
        await state.finish()
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='Вернуться',
                                       callback_data=make_cb_data(category_cb,
                                                                  str(product['enter_ids']['category_id']),
                                                                  product['enter_ids']['place'])))
        await message.answer('Принято', reply_markup=kb)
    except ValueError:
        await message.answer('Неверное значение. Повторите ввод:')
        await CreateProduct.enter_amount.set()


async def append_product(call: types.CallbackQuery, product_id: int, place):
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateProduct.enter_ids.set()
    product = await ProductTools.get_product(product_id)
    ids = {'product_id': product_id,
           'amount': product.amount,
           'category_id': product.category_id,
           'place': place}
    await state.update_data(enter_ids=ids)
    await call.message.edit_text('Сколько докупаем?', reply_markup=None)
    await CreateProduct.append_amount.set()


async def append_product_amount(message: types.Message, state: FSMContext):
    # await message.edit_text('Введите адрес организации', reply_markup=None)
    amount = message.text
    try:
        async with state.proxy() as data:
            data['append_amount'] = int(amount)
        product = await state.get_data()
        print(product)
        await ProductTools.update_product(product_id=product['enter_ids']['product_id'],
                                          amount=product['enter_ids']['amount'] + product['append_amount'],
                                          # material_id=product['enter_name'],
                                          # category_id=product['ids']['category_id'],
                                          # storage_id=product['ids']['storage_id'],
                                          # production_area_id=product['ids']['production_area_id'],
                                          )
        await state.finish()
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='Вернуться',
                                       callback_data=make_cb_data(category_cb,
                                                                  str(product['enter_ids']['category_id']),
                                                                  product['enter_ids']['place'])))
        await message.answer('Принято', reply_markup=kb)
    except ValueError:
        await message.answer('Неверное значение. Повторите ввод:')
        await CreateProduct.append_amount.set()


async def ship_product(call: types.CallbackQuery, product_id: int):
    product = await ProductTools.get_product(product_id)
    name = await ProductTools.get_product_name(product)
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateProduct.enter_ids.set()
    ids = {'product_id': product_id,
           'amount': product.amount,
           'category_id': product.category_id,
           'place': place}
    await state.update_data(enter_ids=ids)
    await call.message.edit_text(f'Имеется {product.amount} товара {name}, сколько отгрузить?', reply_markup=None)
    await CreateProduct.change_amount.set()


def product_handlers_register(dp: Dispatcher):
    dp.register_message_handler(enter_product_name, state=CreateProduct.enter_name)
    dp.register_message_handler(enter_product_amount, state=CreateProduct.enter_amount)
    dp.register_message_handler(append_product_amount, state=CreateProduct.append_amount)

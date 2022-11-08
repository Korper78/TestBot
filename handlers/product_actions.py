from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))
from db_tools.prodarea_utils import ProdAreaTools
from db_tools.product_utils import ProductTools
from db_tools.storage_utils import StorageTools
from handlers.storage_actions import storage_in
from keyboards.inline_kb import make_cb_data, category_cb, store_action_cb, prod_area_action_cb, create_prod_area_kb, \
    create_storage_kb, create_product_kb, product_cb
from loader import storage


class CreateProduct(StatesGroup):
    # enter_place = State()
    # enter_category = State()
    enter_ids = State()
    enter_name = State()
    enter_raw = State()
    enter_amount = State()
    append_amount = State()
    ship_amount = State()
    move_amount = State()


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
    products_in_cat = await ProductTools.get_products_by_category(supercategory)
    names_in_cat = set([await ProductTools.get_product_name(product)
                        for product in products_in_cat])
    # if product.storage_id != storage_id and product.production_area_id != prodarea_id]))
    local_names = set([await ProductTools.get_product_name(product)
                       for product in products])
    names = names_in_cat - local_names
    ids = {'category_id': supercategory,
           'storage_id': storage_id,
           'production_area_id': prodarea_id,
           'place': place,
           'names': names}
    await state.update_data(enter_ids=ids)
    print(await state.get_data())
    # names = await ProductTools.get_product_names()
    await call.message.edit_text('Введите название материала/товара', reply_markup=None)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # kb.add([types.KeyboardButton(text=name.name) for name in names])
    # kb.add([types.KeyboardButton(text=name) for name in names])
    kb.add(*names)
    if names:
        await call.message.answer('или выберите из имеющихся:', reply_markup=kb)
    # await message.answer('Введите или выберите название материала/товара', reply_markup=kb)
    await CreateProduct.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_name)
async def enter_product_name(message: types.Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    if name in data['enter_ids']['names']:
        name_id = [_name.id for _name in await ProductTools.get_product_names() if _name.name == name][0]
    else:
        name_id = await ProductTools.add_product_name(name)
    if name_id:
        res = await ProductTools.add_product(amount=0,
                                             material_id=name_id,
                                             category_id=data['enter_ids']['category_id'],
                                             storage_id=data['enter_ids']['storage_id'],
                                             production_area_id=data['enter_ids']['production_area_id'],
                                             )
        print(res)
        await state.finish()
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='Вернуться',
                                       callback_data=make_cb_data(category_cb,
                                                                  str(data['enter_ids']['category_id']),
                                                                  data['enter_ids']['place'])))
        await message.answer('Принято', reply_markup=kb)

        # async with state.proxy() as data:
        #     data['enter_name'] = name_id
        # await message.answer('Введите количество:', reply_markup=types.ReplyKeyboardRemove())
        # await CreateProduct.enter_amount.set()
    else:
        await message.answer('Такое название уже есть в другой категории. Повторите ввод:')
        await CreateProduct.enter_name.set()


# # @dp.message_handler(state=CreateFoundation.enter_address)
# async def enter_product_amount(message: types.Message, state: FSMContext):
#     # await message.edit_text('Введите адрес организации', reply_markup=None)
#     amount = message.text
#     try:
#         async with state.proxy() as data:
#             data['enter_amount'] = int(amount)
#         product = await state.get_data()
#         print(product)
#         res = await ProductTools.add_product(amount=product['enter_amount'],
#                                              material_id=product['enter_name'],
#                                              category_id=product['enter_ids']['category_id'],
#                                              storage_id=product['enter_ids']['storage_id'],
#                                              production_area_id=product['enter_ids']['production_area_id'],
#                                              )
#         print(res)
#         await state.finish()
#         kb = types.InlineKeyboardMarkup().add(
#             types.InlineKeyboardButton(text='Вернуться',
#                                        callback_data=make_cb_data(category_cb,
#                                                                   str(product['enter_ids']['category_id']),
#                                                                   product['enter_ids']['place'])))
#         await message.answer('Принято', reply_markup=kb)
#     except ValueError:
#         await message.answer('Неверное значение. Повторите ввод:')
#         await CreateProduct.enter_amount.set()
#
#
async def append_product(call: types.CallbackQuery, product_id: int, place):
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateProduct.enter_ids.set()
    product = await ProductTools.get_product(product_id)
    ids = {'product_id': product_id,
           'amount': product.amount,
           'category_id': product.category_id,
           'place': place}
    await state.update_data(enter_ids=ids)
    await call.message.edit_text('Сколько приобрести?', reply_markup=None)
    await CreateProduct.append_amount.set()


async def append_product_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
        async with state.proxy() as data:
            data['append_amount'] = amount
        product = await state.get_data()
        print(product)
        await ProductTools.update_product(product_id=product['enter_ids']['product_id'],
                                          amount=product['enter_ids']['amount'] + product['append_amount'])
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


async def produce_product(call: types.CallbackQuery, product_id: int, place):
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    # match state:
    #     case
    st = await state.get_state()
    print(st, CreateProduct.enter_raw)
    if st == 'CreateProduct:enter_raw':
        async with state.proxy() as data:
            data['enter_raw'].append(product_id)
        await call.message.edit_text('Введите количество:', reply_markup=None)
        await CreateProduct.enter_amount.set()
    else:
        product = await ProductTools.get_product(product_id)
        ids = {'product_id': product_id,
               'amount': product.amount,
               'category_id': product.category_id,
               'prodarea_id': product.production_area_id,
               'place': place}
        # product = await ProductTools.get_product(product_id)
        # prodarea_id = int(product['enter_ids']['place'].split('_')[1])
        # prodarea_id = int(place.split('_')[1])
        products = await ProductTools.get_products_by_prodarea(product.production_area_id)
        products = [(prod, await ProductTools.get_product_name(prod)) for prod in products if prod.id != product.id]
        kb = create_product_kb(products, place, product.category_id)
        del kb.inline_keyboard[-1]
        # kb.add(InlineKeyboardButton(text='Произвести',
        #                             callback_data=make_cb_data(product_cb,
        #                                                        product.id,
        #                                                        place)))
        await CreateProduct.enter_ids.set()
        await state.update_data(enter_ids=ids)
        await CreateProduct.enter_amount.set()
        await state.update_data(enter_amount=[])
        await CreateProduct.enter_raw.set()
        await state.update_data(enter_raw=[])
        await call.message.edit_text('Выберите, из чего произвести:', reply_markup=kb)
        # await CreateProduct.enter_raw.set()


# @dp.message_handler(state=CreateFoundation.enter_address)
async def enter_product_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
        product = await state.get_data()
        if product['enter_ids']['product_id'] == product['enter_raw'][-1]:
            await ProductTools.update_product(product_id=product['enter_ids']['product_id'],
                                              amount=product['enter_ids']['amount'] + amount)
            await state.finish()
            kb = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text='Вернуться',
                                           callback_data=make_cb_data(category_cb,
                                                                      str(product['enter_ids']['category_id']),
                                                                      product['enter_ids']['place'])))
            await message.answer('Принято', reply_markup=kb)
        else:
            prod = await ProductTools.get_product(product['enter_raw'][-1])
            if amount > prod.amount:
                raise ValueError
            async with state.proxy() as data:
                # data['enter_amount'] = int(amount)
                data['enter_amount'].append(amount)
            if amount == prod.amount:
                await ProductTools.del_product(prod)
            else:
                await ProductTools.update_product(product_id=prod.id,
                                                  amount=prod.amount - amount)
            # product = await ProductTools.get_product(product_id)
            # prodarea_id = int(product['enter_ids']['place'].split('_')[1])
            # prodarea_id = int(place.split('_')[1])
            products = await ProductTools.get_products_by_prodarea(product['enter_ids']['prodarea_id'])
            products = [(pr, await ProductTools.get_product_name(pr)) for pr in products if
                        # pr.id != prod.id and pr.id != product['enter_ids']['product_id']]
                        pr.id != product['enter_ids']['product_id'] and pr.id not in product['enter_raw']]
            kb = create_product_kb(products, product['enter_ids']['place'], product['enter_ids']['category_id'])
            del kb.inline_keyboard[-1]
            kb.add(InlineKeyboardButton(text='Произвести',
                                        callback_data=make_cb_data(product_cb,
                                                                   product['enter_ids']['product_id'],
                                                                   product['enter_ids']['place'])))
            await CreateProduct.enter_raw.set()
            await message.answer('Выберите, из чего произвести:', reply_markup=kb)
    except ValueError:
        await message.answer('Неверное значение. Повторите ввод:')
        await CreateProduct.enter_amount.set()


async def ship_product(call: types.CallbackQuery, product_id: int):
    product = await ProductTools.get_product(product_id)
    name = await ProductTools.get_product_name(product)
    # place = 'storage_' + str(product.storage_id) if product.storage_id else 'prodarea_' + str(
    #     product.production_area_id)
    ids = {'product_id': product_id,
           'amount': product.amount}
    # 'category_id': product.category_id,
    # 'place': place}
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateProduct.enter_ids.set()
    await state.update_data(enter_ids=ids)
    await call.message.edit_text(f'Имеется {product.amount} товара {name}, сколько отгрузить?', reply_markup=None)
    await CreateProduct.ship_amount.set()


async def ship_product_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
        async with state.proxy() as data:
            data['ship_amount'] = amount
        prod = await state.get_data()
        print(prod)
        new_amount = prod['enter_ids']['amount'] - prod['ship_amount']
        if new_amount < 0 or new_amount == prod['enter_ids']['amount']:
            raise ValueError()
            # await message.answer('Столько нет в наличии. Повторите ввод:')
            # await CreateProduct.append_amount.set()
        else:
            product = await ProductTools.get_product(prod['enter_ids']['product_id'])
            name = await ProductTools.get_product_name(product)
            shiped_product = await ProductTools.get_product_by_shipment(product.storage_id,
                                                                        product.production_area_id,
                                                                        name)
            if shiped_product is None:
                shiped_product = await ProductTools.add_product(amount=prod['ship_amount'],
                                                                material_id=product.material_id,
                                                                category_id=product.category_id,
                                                                storage_id=product.storage_id,
                                                                production_area_id=product.production_area_id,
                                                                is_shipment=True)
                shiped_product = await ProductTools.get_product(shiped_product)
            else:
                await ProductTools.update_product(product_id=shiped_product.id,
                                                  amount=shiped_product.amount + prod['ship_amount'],
                                                  is_shipment=True)
            if new_amount:
                await ProductTools.update_product(product_id=product.id,
                                                  amount=new_amount)
            else:
                await ProductTools.del_product(product)
            await state.finish()
            callback_data = make_cb_data(store_action_cb,
                                         'total',
                                         shiped_product.storage_id) if shiped_product.storage_id else make_cb_data(
                prod_area_action_cb,
                'total',
                shiped_product.production_area_id)
            kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Вернуться',
                                                                             callback_data=callback_data))
            await message.answer('Принято', reply_markup=kb)
    except ValueError:
        await message.answer('Неверное значение. Повторите ввод:')
        await CreateProduct.ship_amount.set()


async def move_product(call: types.CallbackQuery, product_id: int):
    product = await ProductTools.get_product(product_id)
    name = await ProductTools.get_product_name(product)
    ids = {'product_id': product_id,
           'amount': product.amount,
           'name': name}
    if product.storage_id:
        store = await StorageTools.get_storage(product.storage_id)
        prodareas = await ProdAreaTools.get_prodareas(store.foundation_id)
        kb = create_prod_area_kb(prodareas, 0)
        del kb.inline_keyboard[-1]
        # ids['place'] = 'storage_' + str(store.id)
    else:
        prodarea = await ProdAreaTools.get_prodarea(product.production_area_id)
        stores = await StorageTools.get_storages(prodarea.foundation_id)
        kb = create_storage_kb(stores, 0)
        del kb.inline_keyboard[-2:]
        # ids['place'] = 'prodarea_' + str(prodarea.id)
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await call.message.edit_text('Куда отгрузить?', reply_markup=kb)
    await CreateProduct.enter_ids.set()
    await state.update_data(enter_ids=ids)


async def move_product_instance(call: types.CallbackQuery, instance_id: int):
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    ids = await state.get_data()
    ids['enter_ids']['instance_id'] = instance_id
    await state.update_data(enter_ids=ids['enter_ids'])
    await call.message.edit_text(f"Имеется {ids['enter_ids']['amount']} товара {ids['enter_ids']['name']},"
                                 f" сколько переместить?", reply_markup=None)
    await CreateProduct.move_amount.set()


async def move_product_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
        async with state.proxy() as data:
            data['move_amount'] = amount
        prod = await state.get_data()
        print(prod)
        new_amount = prod['enter_ids']['amount'] - prod['move_amount']
        if new_amount < 0 or new_amount == prod['enter_ids']['amount']:
            raise ValueError()
            # await message.answer('Столько нет в наличии. Повторите ввод:')
            # await CreateProduct.append_amount.set()
        else:
            from_product = await ProductTools.get_product(prod['enter_ids']['product_id'])
            name = await ProductTools.get_product_name(from_product)
            # place = prod['enter_ids']['place'].split('_')
            instance_id = prod['enter_ids']['instance_id']
            # if place[0] == 'storage':
            if from_product.storage_id:
                to_products = await ProductTools.get_products_by_prodarea(instance_id)
            else:
                to_products = await ProductTools.get_products_by_storage(instance_id)
            # to_product = [product for product in to_products if await ProductTools.get_product_name(product) == name][0]
            to_product = [product for product in to_products if await ProductTools.get_product_name(product) == name]
            # if to_product is None:
            if not to_product:
                to_product = await ProductTools.add_product(amount=prod['move_amount'],
                                                            material_id=from_product.material_id,
                                                            category_id=from_product.category_id,
                                                            storage_id=None if from_product.storage_id else instance_id,
                                                            production_area_id=None if from_product.production_area_id else instance_id)
                to_product = await ProductTools.get_product(to_product)
            else:
                to_product = to_product[0]
                await ProductTools.update_product(product_id=to_product.id,
                                                  amount=to_product.amount + prod['move_amount'])
            if new_amount:
                await ProductTools.update_product(product_id=from_product.id,
                                                  amount=new_amount)
            else:
                await ProductTools.del_product(from_product)
            await state.finish()
            callback_data = make_cb_data(store_action_cb,
                                         'total',
                                         to_product.storage_id) if to_product.storage_id else make_cb_data(
                prod_area_action_cb,
                'total',
                to_product.production_area_id)
            kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Вернуться',
                                                                             callback_data=callback_data))
            await message.answer('Принято', reply_markup=kb)
    except ValueError:
        await message.answer('Неверное значение. Повторите ввод:')
        await CreateProduct.move_amount.set()


def product_handlers_register(dp: Dispatcher):
    dp.register_message_handler(enter_product_name, state=CreateProduct.enter_name)
    dp.register_message_handler(enter_product_amount, state=CreateProduct.enter_amount)
    dp.register_message_handler(append_product_amount, state=CreateProduct.append_amount)
    dp.register_message_handler(ship_product_amount, state=CreateProduct.ship_amount)
    dp.register_message_handler(move_product_amount, state=CreateProduct.move_amount)

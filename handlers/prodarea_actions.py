from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))
from db_tools.prodarea_utils import ProdAreaTools
from handlers.commands import found_menu


class CreateProdArea(StatesGroup):
    enter_found_id = State()
    enter_name = State()


# async def create_prod_area(call: types.CallbackQuery, found_id: int, state: FSMContext):
async def create_prod_area(call: types.CallbackQuery, found_id: int):
    await call.message.edit_text('Введите название производства', reply_markup=None)
    # await state.set_state(CreateFoundation.enter_name)
    await CreateProdArea.enter_found_id.set()
    state = FSMContext(storage=MemoryStorage(), chat=call.message.chat, user=call.message.from_user.id)
    # CreateProdArea.enter_found_id = found_id
    # async with state.proxy() as data:
    #     data['enter_found_id'] = found_id
    await state.update_data(enter_found_id=found_id)
    await CreateProdArea.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_name)
# async def enter_foundation_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['enter_name'] = message.text
#     await message.answer('Введите адрес организации')
#     # await state.set_state(CreateFoundation.enter_address)
#     await CreateFoundation.enter_address.set()


# @dp.message_handler(state=CreateFoundation.enter_address)
async def enter_prod_area_name(message: types.Message, state: FSMContext):
    # await message.edit_text('Введите адрес организации', reply_markup=None)
    async with state.proxy() as data:
        data['enter_name'] = message.text
    prod_area = await state.get_data()
    print(prod_area)
    # name = await message.text
    # found_id = CreateProdArea.enter_found_id.state
    res = await ProdAreaTools.add_prodarea(name=prod_area['enter_name'],
                                           foundation_id=prod_area['enter_found_id'])
    # res = await ProdAreaTools.add_prodarea(name=name,
    #                                        foundation_id=found_id)
    print(res)
    await state.finish()
    await found_menu(message, prod_area['enter_found_id'])
    # await found_menu(message, found_id)


def prod_area_handlers_register(dp: Dispatcher):
    # dp.register_message_handler(create_prod_area, state=CreateProdArea.enter_found_id)
    dp.register_message_handler(enter_prod_area_name, state=CreateProdArea.enter_name)

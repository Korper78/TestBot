from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))
from db_tools.foundation_utils import FoundTools
from handlers.commands import start_menu


class CreateFoundation(StatesGroup):
    enter_name = State()
    enter_address = State()


# async def create_foundation(call: types.CallbackQuery, state: FSMContext = '*'):
async def create_foundation(message: types.Message):
    await message.edit_text('Введите название организации', reply_markup=None)
    # await state.set_state(CreateFoundation.enter_name)
    await CreateFoundation.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_name)
async def enter_foundation_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['enter_name'] = message.text
    await message.answer('Введите адрес организации')
    # await state.set_state(CreateFoundation.enter_address)
    await CreateFoundation.enter_address.set()


# @dp.message_handler(state=CreateFoundation.enter_address)
async def enter_foundation_address(message: types.Message, state: FSMContext):
    # await message.edit_text('Введите адрес организации', reply_markup=None)
    async with state.proxy() as data:
        data['enter_address'] = message.text
    foundation = await state.get_data()
    print(foundation)
    res = await FoundTools.add_foundation(name=foundation['enter_name'],
                                          address=foundation['enter_address'])
    print(res)
    await state.finish()
    # await message.answer('Спасибо')
    await start_menu(message)


def foundation_handlers_register(dp: Dispatcher):
    dp.register_message_handler(enter_foundation_name, state=CreateFoundation.enter_name)
    dp.register_message_handler(enter_foundation_address, state=CreateFoundation.enter_address)

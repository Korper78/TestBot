from aiogram import types, Dispatcher
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bot import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# cancel_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='found:cancel'))

# from db_tools.category_utils import CategoryTools
from db_tools import CategoryTools
# from handlers.storage_actions import storage_in
# from keyboards.inline_kb import make_cb_data, category_cb
from keyboards import make_cb_data, category_cb
from loader import storage


class CreateCategory(StatesGroup):
    enter_place = State()
    enter_supercategory = State()
    enter_name = State()


# async def create_foundation(call: types.CallbackQuery, state: FSMContext = '*'):
async def create_category(call: types.CallbackQuery, supercategory: int, place: str):
    await call.message.edit_text('Введите название категории', reply_markup=None)
    # await state.set_state(CreateFoundation.enter_name)
    await call.answer()
    state = FSMContext(storage=storage, chat=call.from_user.id, user=call.from_user.id)
    await CreateCategory.enter_place.set()
    await state.update_data(enter_place=place)
    await CreateCategory.enter_supercategory.set()
    await state.update_data(enter_supercategory=supercategory)
    await CreateCategory.enter_name.set()


# @dp.message_handler(state=CreateFoundation.enter_name)
# async def enter_category_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['enter_name'] = message.text
#     await message.answer('Введите адрес организации')
#     # await state.set_state(CreateFoundation.enter_address)
#     await CreateFoundation.enter_address.set()


# @dp.message_handler(state=CreateFoundation.enter_address)
async def enter_category_name(message: types.Message, state: FSMContext):
    # await message.edit_text('Введите адрес организации', reply_markup=None)
    async with state.proxy() as data:
        data['enter_name'] = message.text
    category = await state.get_data()
    print(category)
    res = await CategoryTools.add_category(name=category['enter_name'],
                                          parent_id=category['enter_supercategory'])
    print(res)
    await state.finish()
    kb = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Вернуться',
                                   callback_data=make_cb_data(category_cb,
                                                              str(category['enter_supercategory']),
                                                              category['enter_place'])))
    await message.answer('Принято', reply_markup=kb)
    # await bot.send_message(message.chat.id, 'Спасибо')
    # place = category['enter_place'].split('_')
    # if place[0] == 'storage':
    #     await storage_in(message, int(place[1]), category['enter_supercategory'])
    # elif place[0] == 'prodarea':
    #     await prodarea_produce(message, int(place[1]), category['enter_supercategory'])
    # await start_menu(message)


def category_handlers_register(dp: Dispatcher):
    dp.register_message_handler(enter_category_name, state=CreateCategory.enter_name)

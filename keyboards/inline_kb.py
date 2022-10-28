from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from db_tools.models import Foundation, Category, ProductionArea, Storage

foundation_cb = CallbackData('found', 'choice')
prod_area_cb = CallbackData('prod_area', 'found_id', 'choice')
storage_cb = CallbackData('store', 'found_id', 'choice')
category_cb = CallbackData('cat', 'id', 'choice')
product_cb = CallbackData('prod', 'id', 'choice')
transaction_cb = CallbackData('trans', 'choice')


def make_cb_data(cb: CallbackData, choice: str, obj_id: str = None):
    if obj_id is None:
        return cb.new(choice)
    else:
        return cb.new(obj_id, choice)


def create_found_kb(foundations: list[Foundation]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for foundation in foundations:
        # print(foundation[0])
        cb = make_cb_data(foundation_cb, str(foundation[0].id))
        # cb = foundation_cb.new(str(foundation.id))
        kb.insert(InlineKeyboardButton(text=foundation[0].name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новая организация',
                                   callback_data=make_cb_data(foundation_cb, 'new')))
    # print(foundation_cb.filter())
    return kb


def create_prod_area_kb(prod_areas: list[ProductionArea], found_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for prod_area in prod_areas:
        cb = make_cb_data(prod_area_cb, str(prod_area[0].id), str(found_id))
        kb.insert(InlineKeyboardButton(text=prod_area[0].name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новое производство',
                                   callback_data=make_cb_data(prod_area_cb, 'new', str(found_id))))
    kb.insert(InlineKeyboardButton(text='Назад',
                                   callback_data=make_cb_data(prod_area_cb, 'back', '')))
    return kb


def create_storage_kb(storages: list[Storage], found_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for storage in storages:
        cb = make_cb_data(storage_cb, str(storage[0].id), str(found_id))
        kb.insert(InlineKeyboardButton(text=storage[0].name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новый склад',
                                   callback_data=make_cb_data(storage_cb, 'new', str(found_id))))
    kb.insert(InlineKeyboardButton(text='Назад',
                                   callback_data=make_cb_data(storage_cb, 'back', '')))
    return kb


def create_cat_kb(categories: list[Category]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        cb = make_cb_data(category_cb, str(category[0].id))
        kb.insert(InlineKeyboardButton(text=category[0].name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новая категория',
                                   callback_data=make_cb_data(category_cb, 'new')))
    kb.insert(InlineKeyboardButton(text='Назад',
                                   callback_data=make_cb_data(category_cb, 'back')))
    return kb


def create_product_kb(products: list[Category]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for product in products:
        cb = make_cb_data(product_cb, str(product[0].id))
        kb.insert(InlineKeyboardButton(text=product[0].name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новая категория',
                                   callback_data=make_cb_data(product_cb, 'new')))
    kb.insert(InlineKeyboardButton(text='Назад',
                                   callback_data=make_cb_data(product_cb, 'back')))
    return kb



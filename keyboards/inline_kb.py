from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# from db_tools.models import Foundation, Category, ProductionArea, Storage, Product
from db_tools import Foundation, Category, ProductionArea, Storage, Product

foundation_cb = CallbackData('found', 'choice')
prod_area_cb = CallbackData('prod_area', 'found_id', 'choice')
storage_cb = CallbackData('store', 'found_id', 'choice')
category_cb = CallbackData('cat', 'place', 'choice')
product_cb = CallbackData('prod', 'place', 'choice')
store_action_cb = CallbackData('store_act', 'store_id', 'choice')
prod_area_action_cb = CallbackData('prod_area_act', 'prod_area_id', 'choice')
prod_action_cb = CallbackData('prod_act', 'prod_id', 'choice')


def make_cb_data(cb: CallbackData, choice: str, obj_id: str = None):
    if obj_id is None:
        return cb.new(choice)
    else:
        return cb.new(obj_id, choice)


def create_found_kb(foundations: list[Foundation]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for foundation in foundations:
        # print(foundation[0])
        cb = make_cb_data(foundation_cb, str(foundation.id))
        # cb = foundation_cb.new(str(foundation.id))
        kb.insert(InlineKeyboardButton(text=foundation.name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новая организация',
                                   callback_data=make_cb_data(foundation_cb, 'new')))
    # print(foundation_cb.filter())
    return kb


def create_prod_area_kb(prod_areas: list[ProductionArea], found_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for prod_area in prod_areas:
        # cb = make_cb_data(prod_area_cb, str(prod_area.id), str(found_id))
        cb = make_cb_data(prod_area_cb, str(prod_area.id), str(found_id))
        kb.insert(InlineKeyboardButton(text=prod_area.name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новое производство',
                                   callback_data=make_cb_data(prod_area_cb, 'new', str(found_id))))
    # kb.insert(InlineKeyboardButton(text='Назад',
    #                                callback_data=make_cb_data(prod_area_cb, 'back', '')))
    return kb


def create_storage_kb(storages: list[Storage], found_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for storage in storages:
        # cb = make_cb_data(storage_cb, str(storage.id), str(found_id))
        cb = make_cb_data(storage_cb, str(storage.id), str(found_id))
        kb.insert(InlineKeyboardButton(text=storage.name, callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новый склад',
                                   callback_data=make_cb_data(storage_cb, 'new', str(found_id))))
    kb.insert(InlineKeyboardButton(text='Назад',
                                   callback_data=make_cb_data(storage_cb, 'back', '')))
    return kb


def create_store_action_kb(storage_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='Приход',
                                callback_data=make_cb_data(store_action_cb, 'in', str(storage_id))),
           # InlineKeyboardButton(text='Уход',
           #                      callback_data=make_cb_data(store_action_cb, 'out', str(storage_id))),
           InlineKeyboardButton(text='Итого',
                                callback_data=make_cb_data(store_action_cb, 'total', str(storage_id))),
           InlineKeyboardButton(text='Назад',
                                callback_data=make_cb_data(store_action_cb, 'back', str(storage_id))))
    return kb


def create_prodarea_action_kb(prodarea_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='Произвести',
                                callback_data=make_cb_data(prod_area_action_cb, 'produce', str(prodarea_id))),
           # InlineKeyboardButton(text='Уход',
           #                      callback_data=make_cb_data(prod_area_action_cb, 'out', str(prodarea_id))),
           InlineKeyboardButton(text='Итого',
                                callback_data=make_cb_data(prod_area_action_cb, 'total', str(prodarea_id))),
           InlineKeyboardButton(text='Назад',
                                callback_data=make_cb_data(prod_area_action_cb, 'back', str(prodarea_id))))
    return kb


def create_cat_kb(categories: list[Category], place: str, supercategory: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        cb = make_cb_data(category_cb, str(category.id), place)
        kb.insert(InlineKeyboardButton(text=category.name, callback_data=cb))
    # parent_id = str(supercategory) if supercategory else ''
    parent_id = str(supercategory or '')
    kb.insert(InlineKeyboardButton(text='Новая (под)категория',
                                   callback_data=make_cb_data(category_cb,
                                                              'new_' + parent_id,
                                                              place)))
    # kb.insert(InlineKeyboardButton(text='Отменить',
    #                                callback_data=make_cb_data(category_cb, 'cancel', place)))
    return kb


def create_product_kb(products: list[(Product, str)], place: str, supercategory: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for product in products:
        cb = make_cb_data(product_cb, str(product[0].id), place)
        kb.insert(InlineKeyboardButton(text=f'{product[1]}, {product[0].amount}',
                                       callback_data=cb))
    kb.insert(InlineKeyboardButton(text='Новый товар/материал',
                                   callback_data=make_cb_data(product_cb,
                                                              'new_'+str(supercategory),
                                                              place)))
    # kb.insert(InlineKeyboardButton(text='Отменить',
    #                                callback_data=make_cb_data(product_cb, 'cancel', place)))
    return kb


def create_product_action_kb(product_id: int, name: str, category: str, amount: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.row(InlineKeyboardButton(text=f'{name}, {amount}т\nв категории {category}',
                                callback_data='*'))
    kb.add(InlineKeyboardButton(text='Отгрузить',
                                callback_data=make_cb_data(prod_action_cb, 'ship', str(product_id))),
           InlineKeyboardButton(text='Переместить',
                                callback_data=make_cb_data(prod_action_cb, 'move', str(product_id))))
    return kb

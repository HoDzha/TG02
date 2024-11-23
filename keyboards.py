from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопка 1")],
    [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
    ], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
    [InlineKeyboardButton(text="Новости", callback_data="news")],
    [InlineKeyboardButton(text="Профиль", callback_data="person")]
    ])

inline_kb_more = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])

inline_kb_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data="option1")],
    [InlineKeyboardButton(text="Опция 2", callback_data="option2")],
])

menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
    ], resize_keyboard=True)

inline_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости",  url="https://dzen.ru/news")],
    [InlineKeyboardButton(text="Музыка",  url="https://music.yandex.ru/")],
    [InlineKeyboardButton(text="Видео", url="https://rutube.ru/")]
    ])


test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

options_set = ["Опция 1", "Опция 2"]

async def optioins_keyboard():
    opt_kb = InlineKeyboardBuilder()
    for key in options_set:
       opt_kb.add(InlineKeyboardButton(text=key, callback_data=key))
    return opt_kb.adjust(2).as_markup()

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://ya.ru'))
    return keyboard.adjust(2).as_markup()



async def menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://ya.ru'))
    return keyboard.adjust(2).as_markup()

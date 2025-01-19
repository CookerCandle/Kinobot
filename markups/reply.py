from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from data.translations import Translator

trns = Translator().trns

def admin_menu(lang):
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=trns("Добавить кино", lang)),
                KeyboardButton(text=trns("Удалить кино", lang))
            ],
            [
                KeyboardButton(text=trns("Добавить споснсора", lang)),
                KeyboardButton(text=trns("Удалить споснсора", lang))
            ],
            [
                KeyboardButton(text=trns("Список фильмов", lang)),
                KeyboardButton(text=trns("Список спонсоров", lang))
            ],
            [
                KeyboardButton(text=trns("Отправить рекламу", lang))
            ]

        ],
        resize_keyboard=True,
        input_field_placeholder=trns('Выберите из представленных вариантов', lang),
        one_time_keyboard=True,
        selective=True
    )
    return menu

def rmk():
    return ReplyKeyboardRemove()
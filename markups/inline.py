from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.translations import Translator

trns = Translator().trns

lang_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="rus", callback_data="lang_ru"),
            InlineKeyboardButton(text="uzb", callback_data="lang_uz"),
        ]
    ]
)


def add_lang(lang):
    add_movie_lang = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=trns("Русский", lang), callback_data="movie_ru"),
                InlineKeyboardButton(text=trns("Узбекский", lang), callback_data="movie_uz"),
            ]
        ]
    )
    return add_movie_lang


def add_quality():
    add_movie_qulity = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="360p", callback_data="quality_360"),
                InlineKeyboardButton(text="480p", callback_data="quality_480"),
            ]
        ]
    )
    return add_movie_qulity


def add_code(lang):
    add_movie_code = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=trns("Да", lang), callback_data="code_yes"),
                InlineKeyboardButton(text=trns("Нет", lang), callback_data="code_no"),
            ]
        ]
    )
    return add_movie_code


def movie_quality(data):
    quality_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{quality}p", callback_data=f"movie_qual_{str(message_id)}")for _,quality,message_id in data]           
        ]
    )
    return quality_buttons


def channels(data, lang):
    buttons = [
        [InlineKeyboardButton(text=f"{index + 1}) {name}", url=link)]
        for index, (name, link) in enumerate(data)
    ]
    buttons.append([InlineKeyboardButton(text=trns("Подписался ✅", lang), callback_data="check_subscription")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def del_movie(lang):
    checkker = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=trns("Да", lang), callback_data="del_yes"),
                InlineKeyboardButton(text=trns("Нет", lang), callback_data="del_no"),
            ]
        ]
    ) 
    return checkker


def ad_send_check(lang):
    checkker = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=trns("Отправить", lang), callback_data="ad_yes"),
                InlineKeyboardButton(text=trns("Отмена", lang), callback_data="ad_no"),
            ]
        ]
    ) 
    return checkker

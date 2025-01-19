from aiogram import F, Router, Bot
from aiogram.types import Message

from data.database import Database
from data.translations import Translator


from markups.inline import movie_quality, channels
from config import kino_base

router = Router()
db = Database()
trns = Translator().trns


@router.message(F.text.isdigit())
async def movie_code(message:Message):
    lang = await db.get_lang(message.from_user.id)
    movies = await db.send_movie(message.text, lang)
    if movies:
        await message.answer(f"<b>{movies[0][0]}</b>\n\n{trns('Выбери качество фильма', lang)}", reply_markup=movie_quality(movies))
    else:
        await message.answer(trns("Нет такого фильма", lang))


@router.message()
async def echo(message:Message, bot: Bot):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(trns("Я не понял тебя", lang))


    # data = [('dsvdvd', 't.me/vsvdvvdtf')]
    # await message.answer("vdv", reply_markup=channels(data))

    # await bot.send_chat_action(message.chat.id, "typing")
    # await bot.forward_message(message.from_user.id, kino_base, 23, )
    # await bot.copy_message(message.from_user.id, kino_base, 23)

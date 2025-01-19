from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery
from aiogram.enums.chat_action import ChatAction

from data.database import Database
from data.translations import Translator

from config import kino_base
from markups.inline import channels

db=Database()
router = Router()
trns = Translator().trns


@router.callback_query(F.data.startswith("lang_"))
async def set_lanaguage(callback: CallbackQuery):
    await callback.message.delete()
    if not await db.user_exists(callback.from_user.id):
        lang = callback.data[5:]
        await db.add_user(callback.from_user.id, lang)
        await callback.message.answer(trns('Успешная регистрация', lang))
    else:
        lang = callback.data[5:]
        await db.set_lang(callback.from_user.id, lang)
        lang = await db.get_lang(callback.from_user.id)
        await callback.message.answer(trns('Язык изменен', lang))


@router.callback_query(F.data.startswith("movie_qual_"))
async def send_movie(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    movie_id = callback.data[11:]
    await bot.send_chat_action(callback.from_user.id, ChatAction.UPLOAD_VIDEO)
    await bot.copy_message(callback.from_user.id, kino_base, movie_id)


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):
    await callback.message.delete()
    sponsors = await db.get_sponsors()
    lang = await db.get_lang(callback.from_user.id)
    not_subscribed = []

    if sponsors:
        for name, link, member in sponsors:
            try:
                chat_member = await callback.bot.get_chat_member(member, callback.from_user.id)
                if chat_member.status == 'left':
                    not_subscribed.append((name, link))
            except:
                pass

    if not_subscribed:
        await callback.message.answer(trns("Чтобы пользоватся ботом, подпишись на каналы", lang), reply_markup=channels(not_subscribed, lang))
    else:
        await callback.message.answer(trns("Спасибо за подписку! Теперь вы можете пользоваться ботом", lang))
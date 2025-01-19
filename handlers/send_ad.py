from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from data.database import Database
from data.translations import Translator
from utils.states import SendAd

from markups.inline import ad_send_check

router = Router()
db = Database()
trn = Translator().trns


@router.callback_query(SendAd.check, F.data.startswith("ad_"))
async def send_ad_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    lang = await db.get_lang(callback.from_user.id)
    users = await db.get_users() 
    for user in users:
        try:
            await callback.bot.copy_message(user[0], callback.from_user.id, data["ad"])
        except:
            pass
    await state.clear()
    await callback.message.answer(trn("Реклама отправлена", lang))


@router.message(SendAd.ad)
async def send_ad(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await state.update_data(ad=message.message_id)
    await state.set_state(SendAd.check)
    await message.answer(trn("Отправить рекламу?", lang), reply_markup=ad_send_check(lang))
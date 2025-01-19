from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.database import Database
from data.translations import Translator
from utils.states import DelSponsor

router = Router()
db = Database() 
trns = Translator().trns


@router.message(DelSponsor.name)
async def del_sponsor(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    sponsors = await db.get_sponsors()
    sponsor = [sponsor[0] for sponsor in sponsors]
    if message.text in sponsor:
        await db.del_sponsor(message.text)
        await message.answer(trns("Спонсор удален", lang))
        await state.clear()
    else:
        await message.answer(trns("Такого спонсора нет", lang))
    
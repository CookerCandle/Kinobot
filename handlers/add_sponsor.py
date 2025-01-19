from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.database import Database
from data.translations import Translator
from utils.states import AddSponsor


from data.message_effect import message_effect as effect


router = Router()
db = Database()
trns = Translator().trns


@router.message(AddSponsor.name)
async def sponsor_name(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await state.update_data(name=message.text)
    await state.set_state(AddSponsor.link)
    await message.answer(trns("Отправь ссылку на канал", lang))


@router.message(AddSponsor.link)
async def sponsor_link(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await state.update_data(link=message.text) 
    await state.set_state(AddSponsor.member)
    await message.answer(trns("Отправь ID канала \n(В начало -100 если это канал или группа)"))


@router.message(AddSponsor.member, F.text.lstrip('-').isdigit())
async def sponsor_member(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)  
    await state.update_data(member=int(message.text))
    data = await state.get_data()
    await state.clear()
    await db.add_sponsor(data["name"], data["link"], data["member"])

    await message.answer(trns("Спонсор добавлен",lang), message_effect_id=effect['fire'])
    await message.answer(trns("Не забудь добавить бота на канал в качестве админа", lang))

    

@router.message(AddSponsor.member)
async def sponsor_member_incorrect(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(trns("Отправь числовое значения", lang))
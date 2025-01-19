from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.database import Database
from data.translations import Translator
from utils.states import AddMovie, AdminHandler, AddSponsor, DelMovie, DelSponsor, SendAd

from config import admin
from markups.reply import rmk

router = Router()
db = Database()
trns = Translator().trns

@router.message(F.from_user.id.in_(admin), AdminHandler.start)
async def menu_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = await db.get_lang(message.from_user.id)
    if message.text == trns('Добавить кино', lang):
        await state.set_state(AddMovie.name)
        await message.answer(trns("Название кино", lang), reply_markup=rmk())
    elif message.text == trns('Добавить споснсора', lang):
        await state.set_state(AddSponsor.name)
        await message.answer(trns("Введи название канала", lang), reply_markup=rmk())
    elif message.text == trns("Удалить кино", lang):
        await state.set_state(DelMovie.name)
        await message.answer(trns("Отправь код фильма для удаления", lang), reply_markup=rmk())
    elif message.text == trns("Удалить споснсора", lang):
        await state.set_state(DelSponsor.name)
        sponsors = await db.get_sponsors() 
        if not sponsors:
            await message.answer(trns("Спонсоров нет", lang))
            await state.clear()
            return
        formated_sponsors = "\n".join(f"{index + 1}) {sponsor[0]} {sponsor[1]}" for index, sponsor in enumerate(sponsors))
        await message.answer(f"{trns('Выбери спонсора для удаления:', lang)}\n{formated_sponsors}")
    elif message.text == trns("Список фильмов", lang):
        movies = await db.get_movies()
        if movies:
            formatedt_movies = "\n".join(f"{index + 1}) {movie[0]} [{movie[1]}]" for index, movie in enumerate(movies))
            await message.answer(f"{trns('Список фильмов:', lang)}\n{formatedt_movies}")
        else:
            await message.answer(trns("Фильмов нет", lang))
    elif message.text == trns("Список спонсоров", lang):
        sponsors = await db.get_sponsors()
        if sponsors:
            formated_sponsors = "\n".join(f"{index + 1}) {sponsor[0]} {sponsor[1]}" for index, sponsor in enumerate(sponsors))
            await message.answer(f"{trns('Список спонсоров:', lang)}\n{formated_sponsors}")
        else:
            await message.answer(trns("Спонсоров нет", lang))   

    elif message.text == "Отправить рекламу":
        await state.set_state(SendAd.ad)
        await message.answer(trns("Отправь сообщения, оно будет всем переслано", lang), reply_markup=rmk())

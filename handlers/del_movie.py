from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from data.database import Database
from data.translations import Translator
from utils.states import DelMovie

from data.message_effect import message_effect as effect
from markups.inline import del_movie as dell

router = Router()
db = Database()
trns = Translator().trns


@router.message(DelMovie.name, F.text.isdigit())
async def del_movie(message: Message, state: FSMContext):
    lang = db.get_lang(message.from_user.id)
    await state.update_data(name=message.text)
    movie = await db.get_movie_data(int(message.text))
    formatted_movies = "\n".join(f"{index + 1}) {name} {code} {language} {quality}"
                            for index, (name, code, language, quality) in enumerate(movie))
    
    await message.answer(f"{trns('Список фильмов под этим айди', lang)}: {message.text}\n\n{formatted_movies}\n\n{trns('Вы точно хотите их удалить?', lang)}", 
                         reply_markup=dell(lang))


@router.callback_query(DelMovie.name, F.data.startswith("del_"))
async def del_check(callback: CallbackQuery, state: FSMContext):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.delete()
    data = await state.get_data()
    await state.clear()

    if callback.data == "del_yes":
        await db.del_movie(data['name'])
        await callback.message.answer(trns("Кино успешно удалено", lang), message_effect_id=effect['dislike'])
    else:
        await callback.message.answer(trns("Удаления отменено", lang), message_effect_id=effect['like'])


@router.message(DelMovie.name)
async def del_movie_incorrect(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(trns("Отправь число", lang))
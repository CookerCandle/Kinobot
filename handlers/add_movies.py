from aiogram import F, Router, Bot
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext

from data.database import Database
from data.translations import Translator
from utils.states import AddMovie

from markups.inline import add_lang, add_quality, add_code
from config import kino_base
from data.message_effect import message_effect as effect

router = Router()
db = Database()
trns = Translator().trns


@router.message(AddMovie.name)
async def name_movie(message:Message, state:FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await state.update_data(name=message.text)
    await state.set_state(AddMovie.code)
    await message.answer(trns("Код кино (придумай)", lang))


@router.callback_query(AddMovie.code, F.data.startswith("code_"))
async def code_movie_update(callback:CallbackQuery, state:FSMContext):
    lang = await db.get_lang(callback.from_user.id)
    await callback.message.delete()
    if callback.data == "code_yes":
        data = await state.get_data()
        await state.update_data(code=data["code"])
        await state.set_state(AddMovie.language)
        await callback.message.answer(trns("Выбери язык", lang), reply_markup=add_lang(lang))
    else:
        await state.set_state(AddMovie.code)
        await callback.message.answer(trns("Отправь другой код", lang))


@router.message(AddMovie.code)
async def code_movie(message:Message, state:FSMContext):
    lang = await db.get_lang(message.from_user.id)   
    if message.text.isdigit():
        if not await db.get_movie_data(message.text):
            await state.update_data(code=message.text)
            await state.set_state(AddMovie.language)
            await message.answer(trns("Выбери язык", lang), reply_markup=add_lang(lang))
        else:
            movie_data = await db.get_movie_data(message.text)
            formatted_movies = "\n".join(f"{index + 1}) {name} {code} {language} {quality}"
                                         for index, (name, code, language, quality) in enumerate(movie_data))
            await state.update_data(code=message.text)
            await message.answer(f"{trns('Фильм с таким кодом уже существует', lang)}\n{formatted_movies}")
            await message.answer(trns("Если фильм является одним и тем же, нажмите на кнопку да"), reply_markup=add_code(lang))
    else:
        await message.answer(trns("Только цифры", lang))


@router.callback_query(AddMovie.language, F.data.startswith("movie_"))
async def lang_movie(callback:CallbackQuery, state: FSMContext):
    lang = await db.get_lang(callback.from_user.id)
    await callback.message.delete()
    await state.update_data(language=callback.data[6:])
    await state.set_state(AddMovie.quality)
    await callback.message.answer(trns("Выбери качество фильма", lang), reply_markup=add_quality())


@router.callback_query(AddMovie.quality, F.data.startswith("quality_"))
async def lang_movie(callback:CallbackQuery , state: FSMContext):
    lang = await db.get_lang(callback.from_user.id)
    await callback.message.delete()
    await state.update_data(quality=callback.data[8:])
    await state.set_state(AddMovie.movie)
    await callback.message.answer(trns("Отправь фильм (mp4)", lang))


@router.message(AddMovie.movie, F.video)
async def video_movie(message: Message, state: FSMContext, bot: Bot):
    lang = db.get_lang(message.from_user.id)
    video = message.video
    data = await state.get_data()
    await state.clear()
    formatted_text = "\n".join([f"{key}: {value}" for key, value in data.items()])

    movie_id = await bot.send_video(kino_base, video.file_id)
    await bot.send_message(kino_base, formatted_text, reply_to_message_id=movie_id.message_id)

    await db.add_movie(data['name'], data['code'], data['language'], data['quality'], movie_id.message_id)

    await message.answer(trns("Кино успешно добавлен", lang), message_effect_id=effect['done'])
    

@router.message(AddMovie.movie, ~F.video)
async def video_movie_incorret(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(trns('Отправь фильм (mp4)', lang))

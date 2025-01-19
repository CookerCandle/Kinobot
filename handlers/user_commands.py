from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.fsm.context import FSMContext

from markups.inline import lang_menu

from data.translations import Translator
from data.database import Database
from config import admin

router = Router()
trns = Translator().trns
db = Database()



@router.message(CommandStart())
async def start(message: Message, state: FSMContext, bot: Bot):
    lang = await db.get_lang(message.from_user.id)
    await state.clear()
    await message.answer(trns("Отправь код фильма", lang))

    commands = [BotCommand(command="start", description="Старт"),
                BotCommand(command="lang", description="Изменить язык")]
    if message.from_user.id in admin:
        commands.append(BotCommand(command="admin", description="Админ панель"))
    
    await bot.set_my_commands(commands, BotCommandScopeDefault())


@router.message(Command("lang"))
async def lang(message: Message):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(trns("Изменения языка:", lang), reply_markup=lang_menu)
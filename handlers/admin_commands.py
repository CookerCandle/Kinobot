from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from data.database import Database
from data.translations import Translator
from utils.states import AdminHandler

from config import admin
from markups.reply import admin_menu

router = Router()
db = Database()
trns = Translator().trns



@router.message(Command("admin"), F.from_user.id.in_(admin))
async def admin(message: Message, state: FSMContext):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(trns("Админ панель", lang), reply_markup=admin_menu(lang))
    await state.set_state(AdminHandler.start)


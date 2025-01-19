from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from data.database import Database
from markups.inline import lang_menu

db = Database()

class CheckRegistration(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        
        if not await db.user_exists(event.from_user.id):
            await db.add_user(event.from_user.id)
            # await event.answer("Выберите язык - Set language", reply_markup=lang_menu)
        else:
            return await handler(event, data)
    
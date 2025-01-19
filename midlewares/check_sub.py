from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from data.database import Database
from data.translations import Translator

from markups.inline import channels

db = Database()
trns = Translator().trns

class CheckSubscription(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        sponsors = await db.get_sponsors() # [(name, link, member), (name, link, member)]
        lang = await db.get_lang(event.from_user.id)
        not_subscribed = []
        if sponsors:
            for name, link, member in sponsors:
                try:
                    chat_member = await event.bot.get_chat_member(member, event.from_user.id)
                    if chat_member.status == 'left':
                        not_subscribed.append((name, link))
                except:
                    pass
        if not_subscribed:
            await event.answer(trns("Чтобы пользоватся ботом, подпишись на каналы", lang), reply_markup=channels(not_subscribed, lang))
            return
        return await handler(event, data)
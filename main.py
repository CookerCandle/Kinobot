import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import (
    user_commands, admin_commands, add_movies,
    add_sponsor, del_movie, admin_messages, user_messages,
    del_sponsors, send_ad
)
from callbacks import call

from midlewares.check_user import CheckRegistration
from midlewares.check_private import PrivateChat
from midlewares.check_sub import CheckSubscription

from config import config as cfg
from data.database import Database


async def main():
    logging.basicConfig(level=logging.INFO)
    db = Database()  # Создаем экземпляр класса Database
    # session = AiohttpSession(proxy="http://proxy.server:3128/")
    bot = Bot(token=cfg.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # ,session=session
    dp = Dispatcher()

    dp.message.middleware(PrivateChat())
    dp.message.middleware(CheckRegistration())
    dp.message.middleware(CheckSubscription())

    dp.include_routers(
        call.router,
        user_commands.router,
        admin_commands.router,
        send_ad.router,
        add_movies.router,
        add_sponsor.router,
        del_movie.router,
        del_sponsors.router,
        admin_messages.router,
        user_messages.router,
    )
    
    await db.initialize()  # Инициализация базы данных
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main()) 

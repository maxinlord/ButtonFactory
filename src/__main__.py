import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from bot.handlers import setup_message_routers
from bot.middlewares import DBSessionMiddleware
from bot.db import Base
from init_db import _sessionmaker, _engine
import config


bot: Bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def on_startup(_engine: AsyncEngine) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shutdown(session: AsyncSession) -> None:
    await session.close_all()




async def set_default_commands(bot: Bot):
    await bot.set_my_commands([ 
        BotCommand(command="start", description='все сначала'),
        BotCommand(command="post", description='новый пост'),
        BotCommand(command="addchat", description='добавить канал'),
    ])




async def main() -> None:

    dp = Dispatcher(_engine=_engine, storage=MemoryStorage())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.callback_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))

    message_routers = setup_message_routers()
    dp.include_router(message_routers)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

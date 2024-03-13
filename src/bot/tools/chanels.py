
from dataclasses import dataclass
from typing import List

from sqlalchemy import select
from init_db import _sessionmaker_for_func
from bot.db import Chat


async def get_all_chanels():
    async with _sessionmaker_for_func() as session:
        return await session.scalars(select(Chat))
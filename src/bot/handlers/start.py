from pprint import pprint
from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext



router = Router()


@router.message(CommandStart())
async def start(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text='Нажми на команду -> /post', reply_markup=types.ReplyKeyboardRemove())

# @router.message()
# async def anymess(message: Message, session: AsyncSession) -> None:
#     pprint(message)

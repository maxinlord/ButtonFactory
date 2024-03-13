from typing import Any
from aiogram import Router
from aiogram import types, enums
from aiogram.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import ChatState
from bot.keyboards import reply_builder
from aiogram.fsm.context import FSMContext
from bot.db import Chat


router = Router()


@router.message(Command(commands=['addchat']))
async def addchat(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await message.answer(text='Добавь меня в канал и сделай админом', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text='После отправь мне любой пост из канала')
    await state.set_state(ChatState.send_post_from_chat)



@router.message(ChatState.send_post_from_chat)
async def sendp(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    if message.text == 'ДА':
        data = await state.get_data()
        session.add(Chat(id_chat=data['chat'], title=data['chat_title']))
        await session.commit()
        await message.answer(text='Канал добавлен', reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    try:
        bot_member = await message.bot.get_chat_member(chat_id=message.forward_from_chat.id, user_id=message.bot.id)
    except:
        await message.answer(text='Я не админ')
        return
    if bot_member.status != enums.ChatMemberStatus.ADMINISTRATOR:
        await message.answer(text='Я не админ')
        return
    await message.answer(text=f'{message.forward_from_chat.title} ваш канал?', reply_markup=reply_builder(text='ДА'))
    await state.update_data(chat=message.forward_from_chat.id, chat_title=message.forward_from_chat.title)





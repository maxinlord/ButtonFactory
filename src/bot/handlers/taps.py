from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import PostState
from aiogram.fsm.context import FSMContext
from bot.tools import parser, generate_text_shema
from bot.keyboards import inline_builder, reply_builder, choice_chanel_keyboard
from bot.db import Post, ButtonReaction, ButtonQuest

router = Router()


@router.callback_query(F.data.split(':')[0] == 'reaction')
async def reaction(query: CallbackQuery, session: AsyncSession, state: FSMContext) -> None:
    post_id = int(query.data.split(':')[-1])
    reaction_id = int(query.data.split(':')[1])
    reaction = await session.get(ButtonReaction, reaction_id)
    reaction.count_taps += 1
    await session.commit()
    post = await session.get(Post, post_id)
    rows, buttons = await parser(shema=post.text_shema_button, shema_id=post.idpk)
    keyb = inline_builder(rows=rows,
                          buttons=buttons)
    await query.message.edit_reply_markup(reply_markup=keyb)


@router.callback_query(F.data.split(':')[0] == 'quest')
async def quest(query: CallbackQuery, session: AsyncSession, state: FSMContext) -> None:
    quest_id = int(query.data.split(':')[-1])
    quest = await session.get(ButtonQuest, quest_id)
    await query.answer(text=quest.answ, show_alert=True)


@router.callback_query(F.data == 'ignore')
async def ignore(query: CallbackQuery, session: AsyncSession, state: FSMContext) -> None:
    await query.answer()

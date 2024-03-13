from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import PostState
from aiogram.fsm.context import FSMContext
from bot.tools import parser, generate_text_shema
from bot.keyboards import inline_builder, reply_builder, choice_chanel_keyboard
from bot.db import Post, Chat

router = Router()


@router.message(Command(commands=['post']))
async def post(message: Message, session: AsyncSession, state: FSMContext) -> None:
    await message.answer(text='Отправь пост', reply_markup=ReplyKeyboardRemove())
    await state.set_state(PostState.send_post)


@router.message(PostState.send_post)
async def getpost(message: Message, session: AsyncSession, state: FSMContext) -> None:
    await state.update_data(post_id=message.message_id)
    await message.answer(text='Отправь кнопки')
    await state.set_state(PostState.send_buttons)


@router.message(PostState.send_buttons)
async def getbuttons(message: Message, session: AsyncSession, state: FSMContext) -> None:
    if message.text == 'ПОДТВЕРДИТЬ':
        await message.answer(text='Выбери канал для отравки', reply_markup=await choice_chanel_keyboard())
        await state.set_state(PostState.choice_chanel)
        return
    data = await state.get_data()
    shema = await generate_text_shema(message.text)
    post = Post(text_shema_button=shema)
    session.add(post)
    await session.commit()
    rows, buttons = await parser(shema=shema, shema_id=post.idpk)
    keyb = inline_builder(rows=rows,
                          buttons=buttons)
    await state.update_data(keyb=keyb)
    await message.bot.copy_message(chat_id=message.from_user.id,
                                   from_chat_id=message.from_user.id,
                                   message_id=data['post_id'],
                                   reply_markup=keyb)
    await message.answer(text='Если все верно нажми ПОДТВЕРДИТЬ, либо отправь кнопки заново.', reply_markup=reply_builder(text='ПОДТВЕРДИТЬ'))


@router.callback_query(PostState.choice_chanel)
async def send_post_chanel(query: CallbackQuery, session: AsyncSession, state: FSMContext) -> None:
    id_chanel = query.data.split(':')[1]
    data = await state.get_data()
    await query.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    try:
        await query.message.bot.copy_message(chat_id=id_chanel, from_chat_id=query.from_user.id, message_id=data['post_id'], reply_markup=data['keyb'])
    except:
        chanel = await session.scalar(select(Chat).where(Chat.id_chat == int(id_chanel)))
        await session.delete(chanel)
        await session.commit()
        await query.message.answer(text='Я не смог отправить пост(', reply_markup=ReplyKeyboardRemove())
        return
    await query.message.answer(text='Пост отправлен', reply_markup=ReplyKeyboardRemove())

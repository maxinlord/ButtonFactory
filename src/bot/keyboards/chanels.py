from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.tools import ButtonData, get_all_chanels


async def choice_chanel_keyboard():
    kb = InlineKeyboardBuilder()
    for channel in await get_all_chanels():
        kb.button(text=channel.title, callback_data=f'chanel:{channel.id_chat}')
    kb.adjust(2)
    return kb.as_markup()
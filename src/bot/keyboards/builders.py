from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.tools import ButtonData

def reply_builder(
    text: str | list[str],
    sizes: int | list[int] = 2,
    **kwargs
) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()

    text = [text] if isinstance(text, str) else text
    sizes = [sizes] if isinstance(sizes, int) else sizes

    [
        builder.button(text=txt)
        for txt in text
    ]

    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True, **kwargs)


def inline_builder(
    buttons: list[ButtonData],
    rows: list[int] = [1],
):
    builder = InlineKeyboardBuilder()

    for button in buttons:
        match button.type:
            case 'reaction':
                builder.button(text=button.text, callback_data=button.data)
            case 'link':
                builder.button(text=button.text, url=button.data)
            case 'text':
                builder.button(text=button.text, callback_data=button.data)
            case 'quest':
                builder.button(text=button.text, callback_data=button.data)
            case _:
                builder.button(text=button.text, callback_data=button.data)

    builder.adjust(*rows)
    return builder.as_markup()

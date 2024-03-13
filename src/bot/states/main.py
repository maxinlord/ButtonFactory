from aiogram.fsm.state import StatesGroup, State


class PostState(StatesGroup):
    send_post = State()
    send_buttons = State()
    choice_chanel = State()

class ChatState(StatesGroup):
    send_post_from_chat = State()
    confirm_chat = State()
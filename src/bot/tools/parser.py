
from dataclasses import dataclass
from typing import List
from init_db import _sessionmaker_for_func
from bot.db import ButtonReaction, ButtonQuest

@dataclass
class ButtonData:
    text: str
    type: str = 'reaction'
    data: str = 'ignore'
    id: int = None

async def parser(shema: str, shema_id: int) -> tuple[list, list[ButtonData]]:
    rows = []
    buttons: List[ButtonData] = []
    for _ in shema.split('\n'):
        counter = 0
        for button in _.split(','):
            if not button:
                continue
            prefix, body = button.strip().split(' ', 1)
            match prefix:
                case 'р':
                    async with _sessionmaker_for_func() as session:
                        button_obj = await session.get(ButtonReaction, int(body))
                        reaction = f'{button_obj.reaction} {button_obj.count_taps}'
                        buttons.append(ButtonData(text=reaction, data=f'reaction:{body}:{shema_id}'))
                case 'с':
                    link, text_mask = body.split('&')
                    buttons.append(ButtonData(text=text_mask, data=link, type='link'))
                case 'т':
                    buttons.append(ButtonData(text=body, type='text'))
                case 'к':
                    async with _sessionmaker_for_func() as session:
                        button_obj = await session.get(ButtonQuest, int(body))
                        buttons.append(ButtonData(text=button_obj.text, data=f'quest:{body}'))
                case _:
                    buttons.append(ButtonData(text=body, type='text'))
            counter+=1
        rows.append(counter)
    return rows, buttons

async def generate_text_shema(text: str) -> str:
    shema_text = []
    for _ in text.split('\n'):
        str_list = []
        for button in _.split(','):
            prefix, body = button.strip().split(' ', 1)
            match prefix:
                case 'р':
                    async with _sessionmaker_for_func() as session:
                        button_obj = ButtonReaction(reaction=body)
                        session.add(button_obj)
                        await session.commit()
                        str_list.append(f'{prefix} {button_obj.idpk}')
                case 'с':
                    str_list.append(f'{prefix} {body}')
                case 'т':
                    str_list.append(f'{prefix} {body}')
                case 'к':
                    text_quest, answ = body.split('&')
                    async with _sessionmaker_for_func() as session:
                        button_obj = ButtonQuest(text=text_quest, answ=answ)
                        session.add(button_obj)
                        await session.commit()
                        str_list.append(f'{prefix} {button_obj.idpk}')
                case _:
                    str_list.append(f'{prefix} {body}')
        shema_text.append(','.join(str_list))      
    return '\n'.join(shema_text)
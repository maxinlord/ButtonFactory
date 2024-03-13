
from datetime import datetime
from typing import List
from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    DECIMAL,
    DateTime,
    Boolean,
    ForeignKey,
)
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class ButtonReaction(Base):
    __tablename__ = "buttons_reaction"

    reaction: Mapped[str] = mapped_column(String(length=64))
    count_taps: Mapped[int] = mapped_column(Integer, default=0)

class ButtonQuest(Base):
    __tablename__ = "buttons_quest"

    text: Mapped[str] = mapped_column(String(length=64))
    answ: Mapped[str] = mapped_column(String(length=64))


class Chat(Base):
    __tablename__ = "chats"

    id_chat: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(length=64))

class Post(Base):
    __tablename__ = "posts"

    text_shema_button: Mapped[str] = mapped_column()
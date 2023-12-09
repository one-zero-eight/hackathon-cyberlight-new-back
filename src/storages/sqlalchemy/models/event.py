__all__ = []

from datetime import datetime
from typing import Optional

from sqlalchemy import Date

from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.models.__mixin__ import IdMixin

from src.storages.sqlalchemy.utils import *


class Event(Base, IdMixin):
    """
    Сущность события
    """

    __tablename__ = "event"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    date_start: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    date_end: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    battle_pass_only: Mapped[bool] = mapped_column(nullable=False, default=False)
    participants: Mapped[Optional[list["PersonalAccount"]]] = relationship(
        "PersonalAccount", secondary="event_participants", lazy="selectin"
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)


class EventParticipants(Base):
    """
    Связка Event & PersonalAccount
    """

    __tablename__ = "event_participants"

    event_id: Mapped[int] = mapped_column(ForeignKey(Event.id), primary_key=True)
    personal_account_id: Mapped[int] = mapped_column(ForeignKey("personal_account.user_id"), primary_key=True)

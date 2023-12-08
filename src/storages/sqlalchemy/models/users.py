__all__ = ["User", "UserTaskAnswer"]

import datetime
from enum import StrEnum

from sqlalchemy import Enum
from sqlalchemy.sql.functions import now

from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.utils import *


class UserRole(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


class User(Base, IdMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[str] = mapped_column(unique=True)

    password_hash: Mapped[str] = mapped_column(nullable=False)

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.DEFAULT)


class UserTaskAnswer(Base, IdMixin):
    __tablename__ = "user_task_answers"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    is_correct: Mapped[bool] = mapped_column(nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=now())

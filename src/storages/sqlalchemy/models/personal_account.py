__all__ = [
    "PersonalAccount",
    "BattlePass",
    "LevelRewards",
    "PersonalAccountBattlePasses",
    "Level",
    "Reward",
    "RewardType",
    "Achievement",
    "PersonalAccountAchievements",
    "PersonalAccountRewards",
]

import datetime
from enum import StrEnum
from typing import Optional

from sqlalchemy import Date

from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.models.__mixin__ import IdMixin

from src.storages.sqlalchemy.utils import *


class PersonalAccount(Base):
    """
    Сущность ЛК, связывает юзера и весь мир
    """

    __tablename__ = "personal_account"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    total_exp: Mapped[int] = mapped_column(nullable=False, default=0)
    rewards: Mapped[Optional[list["Reward"]]] = relationship(
        "Reward", secondary="personal_account_rewards", lazy="selectin"
    )
    achievements: Mapped[Optional[list["Achievement"]]] = relationship(
        "Achievement", secondary="personal_account_achievements", lazy="selectin"
    )
    battle_passes: Mapped[Optional[list["BattlePass"]]] = relationship(
        "BattlePass",
        secondary="personal_account_battle_passes",
        lazy="selectin",
        viewonly=True,
        secondaryjoin="and_(BattlePass.id == PersonalAccountBattlePasses.battle_pass_id)",
    )


class BattlePass(Base, IdMixin):
    """
    Глобальная сущность БП
    """

    __tablename__ = "battle_pass"

    name: Mapped[str] = mapped_column(nullable=False)
    date_start: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    date_end: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    levels: Mapped[Optional[list["Level"]]] = relationship("Level", lazy="selectin")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)


class PersonalAccountBattlePasses(Base):
    """
    Прогресс Юзера по БП
    """

    __tablename__ = "personal_account_battle_passes"

    battle_pass_id: Mapped[int] = mapped_column(ForeignKey(BattlePass.id), primary_key=True)
    personal_account_id: Mapped[int] = mapped_column(ForeignKey(PersonalAccount.user_id), primary_key=True)
    experience: Mapped[int] = mapped_column(nullable=False, default=0)  # суммарная экспа юзера по конкретному БП


class Level(Base, IdMixin):
    """
    Сущность Левела, у каждого БП свои уникальные Левелы, для каждого Левела свои Награды
    (Награды можно переиспользовать)
    """

    __tablename__ = "level"

    battle_pass_id: Mapped[int] = mapped_column(ForeignKey(BattlePass.id), nullable=False)
    experience: Mapped[int] = mapped_column(nullable=False)  # необходимое кол-во экспы для уровня
    value: Mapped[int] = mapped_column(nullable=False)  # порядковый номер уровня (первый, второй, и т.д.)
    rewards: Mapped[Optional[list["Reward"]]] = relationship("Reward", secondary="level_rewards", lazy="selectin")


class RewardType(StrEnum):
    """
    Типы наград
    """

    NONE = "none"

    XP = "xp"
    ITEM = "item"


class Reward(Base, IdMixin):
    """
    Награда за левел батлпаса, в принципе одна сущность на все левела
    """

    __tablename__ = "reward"

    name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[RewardType] = mapped_column(nullable=False, default=RewardType.NONE)
    image: Mapped[str] = mapped_column(nullable=True)


class LevelRewards(Base):
    """
    Связка Награда-Уровень
    """

    __tablename__ = "level_rewards"

    level_id: Mapped[int] = mapped_column(ForeignKey(Level.id), primary_key=True)
    reward_id: Mapped[int] = mapped_column(ForeignKey(Reward.id), primary_key=True)
    reward: Mapped["Reward"] = relationship("Reward", viewonly=True, lazy="joined")


class PersonalAccountRewards(Base, IdMixin):
    """
    Награда юзера
    """

    __tablename__ = "personal_account_rewards"

    reward_id: Mapped[int] = mapped_column(ForeignKey(Reward.id))
    personal_account_id: Mapped[int] = mapped_column(ForeignKey(PersonalAccount.user_id))
    count: Mapped[int] = mapped_column(default=1, nullable=True)


class Achievement(Base, IdMixin):
    """
    Ачивка за какое-то действие, присваивается юзеру и показывается в профиле
    """

    __tablename__ = "achievement"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)


class PersonalAccountAchievements(Base):
    """
    Связка Юзера и Ачивок
    """

    __tablename__ = "personal_account_achievements"

    personal_account_id: Mapped[int] = mapped_column(ForeignKey(PersonalAccount.user_id), primary_key=True)
    achievement_id: Mapped[int] = mapped_column(ForeignKey(Achievement.id), primary_key=True)

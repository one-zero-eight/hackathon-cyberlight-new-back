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

from enum import StrEnum
from typing import Optional

from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.models.__mixin__ import IdMixin

from src.storages.sqlalchemy.utils import *


class PersonalAccount(Base):
    """
    Сущность ЛК, связывает юзера и весь мир
    """

    __tablename__ = "personal_account"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    rewards: Mapped[Optional[list["Reward"]]] = relationship(
        "Reward", secondary="personal_account_rewards", back_populates="reward_personal_accounts", lazy="selectin"
    )
    achievements: Mapped[Optional[list["Achievement"]]] = relationship(
        "Achievement", secondary="personal_account_achievements", lazy="selectin"
    )
    battle_passes: Mapped[Optional[list["BattlePass"]]] = relationship(
        "BattlePass", secondary="personal_account_battle_passes", lazy="selectin"
    )


class BattlePass(Base, IdMixin):
    """
    Глобальная сущность БП
    """

    __tablename__ = "battle_pass"

    levels: Mapped[list["Level"]] = relationship("Level", lazy="selectin")
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

    experience: Mapped[int] = mapped_column(nullable=False)  # необходимое кол-во экспы для уровня
    value: Mapped[int] = mapped_column(nullable=False)  # порядковый номер уровня (первый, второй, и т.д.)
    rewards: Mapped[Optional[list["Reward"]]] = relationship(
        "Reward", secondary="level_rewards", back_populates="reward_levels", lazy="selectin"
    )


class RewardType(StrEnum):
    """
    Типы наград
    """

    DEFAULT = "default"

    # TODO: добавить типы


class Reward(Base, IdMixin):
    """
    Награда за левел батлпаса, в принципе одна сущность на все левела
    """

    __tablename__ = "reward"

    name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[RewardType] = mapped_column(nullable=False, default=RewardType.DEFAULT)
    image: Mapped[str] = mapped_column(nullable=True)
    icon: Mapped[str] = mapped_column(nullable=True)


class LevelRewards(Base):
    """
    Связка Награда-Уровень
    """

    __tablename__ = "level_rewards"

    level_id: Mapped[int] = mapped_column(ForeignKey(Level.id), primary_key=True)
    reward_id: Mapped[int] = mapped_column(ForeignKey(Reward.id), primary_key=True)


class PersonalAccountRewards(Base):
    """
    Награда юзера
    """

    __tablename__ = "personal_account_rewards"

    reward_id: Mapped[int] = mapped_column(ForeignKey(Reward.id), primary_key=True)
    personal_account_id: Mapped[int] = mapped_column(ForeignKey(PersonalAccount.user_id), primary_key=True)


class Achievement(Base, IdMixin):
    """
    Ачивка за какое-то действие, присваивается юзеру и показывается в профиле
    """

    __tablename__ = "achievement"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    icon: Mapped[str] = mapped_column(nullable=True)


class PersonalAccountAchievements(Base):
    """
    Связка Юзера и Ачивок
    """

    __tablename__ = "personal_account_achievements"

    personal_account_id: Mapped[int] = mapped_column(ForeignKey(PersonalAccount.user_id), primary_key=True)
    achievement_id: Mapped[int] = mapped_column(ForeignKey(Achievement.id), primary_key=True)

from enum import StrEnum
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy.dialects import postgresql

from src.storages.sqlalchemy.models import Reward
from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.utils import *


class StepType(StrEnum):
    empty = "empty"
    instant = "instant"
    radio = "radio"
    multichoice = "multichoice"
    input = "input"


class ConditionType(StrEnum):
    nothing = "nothing"
    min_level = "min_level"
    reward = "reward"
    battlepass = "battlepass"


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alias: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False, default="")
    content: Mapped[str] = mapped_column(nullable=False, default="")
    difficulty: Mapped[int] = mapped_column(nullable=False, default=0)
    tasks: AssociationProxy[list["Task"]] = association_proxy("task_associations", "task")
    task_associations: Mapped[list["TaskAssociation"]] = relationship(
        "TaskAssociation", lazy="selectin", order_by="TaskAssociation.order"
    )

    condition_type: Mapped[ConditionType] = mapped_column(
        SQLEnum(ConditionType), nullable=False, default=ConditionType.nothing
    )
    recommended_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
    min_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
    reward_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Reward.id), nullable=True, default=None)
    battlepass_id: Mapped[Optional[int]] = mapped_column(ForeignKey("battle_pass.id"), nullable=True, default=None)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alias: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False, default="")
    content: Mapped[str] = mapped_column(nullable=False, default="")
    type: Mapped["StepType"] = mapped_column(SQLEnum(StepType), nullable=False, default=StepType.empty)
    choices: Mapped[list[str]] = mapped_column(postgresql.ARRAY(String), nullable=True, default=None)
    correct_choices: Mapped[list[int]] = mapped_column(postgresql.ARRAY(Integer), nullable=True, default=None)
    input_answers: Mapped[list[str]] = mapped_column(postgresql.ARRAY(String), nullable=True, default=None)
    explanation: Mapped[Optional[str]] = mapped_column(nullable=True)
    exp: Mapped[int] = mapped_column(nullable=False, default=0)
    rewards: AssociationProxy[list["Reward"]] = association_proxy("rewards_associations", "reward")
    rewards_associations: Mapped[list["TaskReward"]] = relationship("TaskReward", lazy="selectin")


class TaskAssociation(Base):
    __tablename__ = "task_association"

    test_id: Mapped[int] = mapped_column(ForeignKey(Lesson.id), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id), primary_key=True)
    order: Mapped[int] = mapped_column(nullable=False, default=0)
    lesson: Mapped[Lesson] = relationship(Lesson, viewonly=True)
    task: Mapped[Task] = relationship(Task, lazy="joined", viewonly=True)


class TaskReward(Base):
    __tablename__ = "task_rewards"

    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id), primary_key=True)
    reward_id: Mapped[int] = mapped_column(ForeignKey(Reward.id), primary_key=True)
    task: Mapped[Task] = relationship(Task, viewonly=True)
    reward: Mapped[Reward] = relationship(Reward, viewonly=True, lazy="joined")
    count: Mapped[int] = mapped_column(nullable=False, default=1)

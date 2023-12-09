import datetime
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field

from src.storages.sqlalchemy.models import StepType, RewardType


class Lesson(BaseModel):
    alias: str
    title: str
    content: str
    difficulty: int
    tasks: list[str] = Field(default_factory=list, description="List of tasks aliases")


class Reward(BaseModel):
    id: int
    type: RewardType = Field(RewardType.NONE, description="Type of the reward")
    name: str
    content: str
    image: Optional[str] = Field(default=None, description="Image of the reward")


class Task(BaseModel):
    class RewardEntry(BaseModel):
        reward_id: int = Field(..., description="ID of the reward")
        count: int = Field(1, description="Count of the reward")

    alias: str = Field(..., description="Alias of the task")
    type: StepType = Field(..., description="Type of the task, need for rendering and validation")

    content: str = Field(..., description="Content of the task")
    title: Optional[str] = Field("", description="Title of the task")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    exp: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")
    rewards: Optional[list[RewardEntry]] = Field(default_factory=list, description="List of reward ids for the task")


class Achievement(BaseModel):
    id: int
    name: str
    description: str
    image: Optional[str] = Field(default=None, description="Image of the achievement")


class Consultant(BaseModel):
    class Timeslot(BaseModel):
        day: int
        start: str
        end: str

    id: int
    name: str
    description: str
    image: Optional[str] = Field(default=None, description="Image of the consultant")
    timeslots: Optional[list["Timeslot"]] = Field(
        default_factory=list, description="List of timeslots for the consultant"
    )


class BattlePass(BaseModel):
    class Level(BaseModel):
        experience: int = Field(
            ..., description="Amount of experience needed to reach this level", examples=[100, 1000, 10000]
        )
        value: int = Field(..., description="Level value: the first, the second...", examples=[1, 2, 3, 4, 5])
        rewards: list[int] = Field(default_factory=list, description="List of rewards for the reaching current level")

    id: int
    name: str
    date_start: datetime.date
    levels: Optional[list["Level"]] = Field(
        default_factory=list, description="List of levels set to current battle pass"
    )
    is_active: bool = Field(..., description="Is current battle pass active for users")


class Predefined(BaseModel):
    lessons: Optional[list[Lesson]] = Field(default_factory=list, description="List of predefined lessons")
    tasks: Optional[list[Task]] = Field(default_factory=list, description="List of predefined tasks")
    rewards: Optional[list[Reward]] = Field(default_factory=list, description="List of predefined rewards")
    achievements: Optional[list[Achievement]] = Field(
        default_factory=list, description="List of predefined achievements"
    )
    consultants: Optional[list[Consultant]] = Field(default_factory=list, description="List of predefined consultants")
    battle_passes: Optional[list[BattlePass]] = Field(
        default_factory=list, description="List of predefined battle passes"
    )

    @classmethod
    def save_schema(cls, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            schema = {"$schema": "http://json-schema.org/draft-07/schema#", **cls.model_json_schema()}
            yaml.dump(schema, f, sort_keys=False)

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        return cls.model_validate(yaml_config)

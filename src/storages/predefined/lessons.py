from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field

from src.storages.sqlalchemy.models import StepType


class Lesson(BaseModel):
    alias: str
    title: str
    content: str
    difficulty: int
    tasks: list[str] = Field(default_factory=list, description="List of tasks aliases")


class Task(BaseModel):
    alias: str = Field(..., description="Alias of the task")
    type: StepType = Field(..., description="Type of the task, need for rendering and validation")

    content: str = Field(..., description="Content of the task")
    title: Optional[str] = Field("", description="Title of the task")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    reward: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")


class PredefinedLessons(BaseModel):
    lessons: Optional[list[Lesson]] = Field(default_factory=list, description="List of predefined lessons")
    tasks: Optional[list[Task]] = Field(default_factory=list, description="List of predefined tasks")

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

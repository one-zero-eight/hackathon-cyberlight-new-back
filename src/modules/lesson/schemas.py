from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.storages.sqlalchemy.models.lesson import StepType


class Answer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_type: StepType = Field(..., description="Type of the task, need for rendering and validation")
    input_answer: Optional[str] = Field(default=None, description="Answer for input task (synonyms)")
    choices: Optional[list[int]] = Field(default=None, description="Choices for multichoice, instant tasks")


class ViewTask(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": dict(
                id=1,
                content="""Что покажет приведенный ниже фрагмент кода?
        ```python
        total = 0
        for i in range(1, 6):
            total += i
            print(total, end="")
        ```                 
        """,
                type="input",
                choices=None,
                correct_choices=None,
                input_answers=["1361015"],
                reward=10,
            )
        },
    )

    id: int = Field(..., description="ID of the task")
    content: str = Field(..., description="Content of the task")
    type: "StepType" = Field(..., description="Type of the task, need for rendering and validation")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    reward: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")

    def check_answer(self, answer: Optional[list[str]]) -> bool:
        if self.type == StepType.input:
            return answer in self.input_answers
        elif self.type == StepType.instant:
            return answer == self.correct_choices
        elif self.type == StepType.radio:
            return answer == self.correct_choices
        elif self.type == StepType.multichoice:
            return answer == self.correct_choices
        else:
            return False


class CreateTask(BaseModel):
    content: str = Field(..., description="Content of the task")
    type: StepType = Field(..., description="Type of the task, need for rendering and validation")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    reward: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")


class UpdateTask(BaseModel):
    content: Optional[str] = Field(None, description="Content of the task")
    type: Optional[StepType] = Field(None, description="Type of the task, need for rendering and validation")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    reward: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")


class ViewLesson(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID of the test", examples=[1])

    difficulty: int = Field(..., description="Difficulty of the test", gt=0, lt=10, examples=[5])
    tasks: list["ViewTask"] = Field(..., description="Tasks of the test (sorted by order)")


class CreateLesson(BaseModel):
    content: str = Field(..., description="Content of the test")
    difficulty: int = Field(..., description="Difficulty of the test", gt=0, lt=10, examples=[5])


class UpdateTest(BaseModel):
    content: Optional[str] = Field(None, description="Content of the test")
    difficulty: Optional[int] = Field(None, description="Difficulty of the test", gt=0, lt=10, examples=[5])


ViewLesson.model_rebuild()

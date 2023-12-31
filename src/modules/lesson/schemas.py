from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.modules.personal_account.schemas import ViewReward
from src.storages.sqlalchemy.models.lesson import StepType, ConditionType


class TaskAnswer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lesson_id: int = Field(..., description="ID of the lesson")
    task_id: int = Field(..., description="ID of the task")
    task_type: StepType = Field(..., description="Type of the task, need for rendering and validation")
    input_answer: Optional[str] = Field(default=None, description="Answer for input task (synonyms)")
    choices: Optional[list[int]] = Field(default=None, description="Choices for multichoice, instant tasks")


class ViewTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID of the task")
    alias: str = Field(..., description="Alias of the task")
    title: Optional[str] = Field("", description="Title of the task")
    content: str = Field(..., description="Content of the task")
    type: "StepType" = Field(..., description="Type of the task, need for rendering and validation")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    exp: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")
    explanation: Optional[str] = Field(default=None, description="Explanation of the answer for the task")
    rewards_associations: Optional[list["RewardAssociation"]] = Field(default_factory=list)

    def check_answer(self, answer: Optional[str | list[str]]) -> bool:
        if self.type == StepType.input and isinstance(answer, str):
            return answer in self.input_answers
        elif self.type == StepType.instant:
            return answer == self.correct_choices
        elif self.type == StepType.radio:
            return answer == self.correct_choices
        elif self.type == StepType.multichoice:
            return answer == self.correct_choices
        elif self.type == StepType.empty:
            return True
        return False


class RewardAssociation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reward: ViewReward = Field(..., description="ID of the reward")
    count: int = Field(..., description="Count of the reward")


class CreateTask(BaseModel):
    alias: str = Field(..., description="Alias of the task")
    content: str = Field(..., description="Content of the task")
    title: Optional[str] = Field("", description="Title of the task")
    type: StepType = Field(..., description="Type of the task, need for rendering and validation")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    explanation: Optional[str] = Field(default=None, description="Explanation of the answer for the task")
    exp: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")


class UpdateTask(BaseModel):
    content: Optional[str] = Field(None, description="Content of the task")
    title: Optional[str] = Field(None, description="Title of the task")
    type: Optional[StepType] = Field(None, description="Type of the task, need for rendering and validation")

    choices: Optional[list[str]] = Field(default=None, description="Choices for multichoice, radio, instant tasks")
    correct_choices: Optional[list[int]] = Field(
        default=None, description="Correct choices for multichoice, instant, radio tasks"
    )
    input_answers: Optional[list[str]] = Field(default=None, description="Answer for input task (synonyms)")
    exp: Optional[int] = Field(default=0, description="Reward for the task (in xp points)")
    explanation: Optional[str] = Field(default=None, description="Explanation of the answer for the task")


class ViewLesson(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID of the lesson", examples=[1])
    alias: str = Field(..., description="Alias of the lesson", examples=["lesson"])
    title: Optional[str] = Field("", description="Title of the lesson")
    content: str = Field(..., description="Content of the lesson")
    difficulty: int = Field(..., description="Difficulty of the lesson", gt=-1, lt=10, examples=[5])
    tasks: list["ViewTask"] = Field(..., description="Tasks of the lesson (sorted by order)")

    condition_type: ConditionType = Field(..., description="Type of condition for lesson")
    recommended_level: Optional[int] = Field(None, description="Recommended level for lesson")
    min_level: Optional[int] = Field(None, description="Min level for lesson")
    reward_id: Optional[int] = Field(None, description="Needed reward id for lesson")
    battlepass_id: Optional[int] = Field(None, description="Battle pass id for lesson")


class CreateLesson(BaseModel):
    alias: str = Field(..., description="Alias of the lesson")
    title: Optional[str] = Field("", description="Title of the lesson")
    content: str = Field(..., description="Content of the lesson")
    difficulty: int = Field(..., description="Difficulty of the lesson", gt=-1, lt=10, examples=[5])

    condition_type: ConditionType = Field(ConditionType.nothing, description="Type of condition for lesson")
    recommended_level: Optional[int] = Field(None, description="Recommended level for lesson")
    min_level: Optional[int] = Field(None, description="Min level for lesson")
    reward_id: Optional[int] = Field(None, description="Needed reward id for lesson")
    battlepass_id: Optional[int] = Field(None, description="Battle pass id for lesson")


class UpdateLesson(BaseModel):
    title: Optional[str] = Field(None, description="Title of the lesson")
    content: Optional[str] = Field(None, description="Content of the lesson")
    difficulty: Optional[int] = Field(None, description="Difficulty of the lesson", gt=-1, lt=10, examples=[5])


ViewLesson.model_rebuild()

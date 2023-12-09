__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.api.dependencies import (
    DEPENDS_LESSON_REPOSITORY,
    DEPENDS_VERIFIED_REQUEST,
    DEPENDS_USER_REPOSITORY,
    DEPENDS_REWARD_REPOSITORY,
    DEPENDS_PERSONAL_ACCOUNT_REPOSITORY,
)
from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult
from src.modules.lesson.repository import LessonRepository
from src.modules.lesson.schemas import (
    ViewLesson,
    CreateLesson,
    TaskAnswer,
    ViewTask,
    CreateTask,
    UpdateLesson,
    UpdateTask,
)
from src.modules.personal_account.repository import RewardRepository, PersonalAccountRepository
from src.modules.user.repository import UserRepository

router = APIRouter(prefix="/lessons", tags=["Lesson"])


class TaskSolveResult(BaseModel):
    success: bool
    rewards: list[int] = Field(default_factory=list)


@router.post("/solve")
async def solve(
    answer: TaskAnswer,
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    personal_account: Annotated[PersonalAccountRepository, DEPENDS_PERSONAL_ACCOUNT_REPOSITORY],
    reward_repository: Annotated[RewardRepository, DEPENDS_REWARD_REPOSITORY],
    task_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY],
) -> TaskSolveResult:
    task = await task_repository.read_task(answer.task_id)

    if task is None:
        raise ObjectNotFound()
    if task.type == "input":
        success = task.check_answer(answer.input_answer)
    else:
        success = task.check_answer(answer.choices)

    await user_repository.submit_answer_for_task(
        user_id=verification.user_id, lesson_id=answer.lesson_id, task_id=answer.task_id, is_correct=success
    )

    if success and task.rewards_associations:
        await reward_repository.add_rewards_to_personal_account(
            verification.user_id, [(r.reward.id, r.count) for r in task.rewards_associations]
        )
        return TaskSolveResult(success=success, rewards=[r.reward.id for r in task.rewards_associations])
    elif success:
        await personal_account.increase_exp(verification.user_id, task.exp)

    return TaskSolveResult(success=success)


class LessonProgress(BaseModel):
    lesson_id: int
    is_available: bool = False


@router.get("/my-progress")
async def get_my_progress(
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    personal_account: Annotated[PersonalAccountRepository, DEPENDS_PERSONAL_ACCOUNT_REPOSITORY],
) -> list[ViewLesson]:
    ...


# ----------------- Lesson -----------------
@router.post("/", status_code=201)
async def post_lesson(
    data: CreateLesson, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewLesson:
    obj = await lesson_repository.create_lesson(data)
    return obj


@router.get("/", response_model=list[ViewLesson])
async def get_all_lessons(
    lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> list[ViewLesson]:
    return await lesson_repository.read_all_lessons()


@router.get("/by-alias/{alias}")
async def get_one_lesson_by_alias(
    alias: str, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewLesson:
    obj = await lesson_repository.read_lesson_by_alias(alias)

    if obj is None:
        raise ObjectNotFound()

    return obj


@router.get("/{lesson_id}")
async def get_one_lesson(
    lesson_id: int, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewLesson:
    obj = await lesson_repository.read_lesson(lesson_id)

    if obj is None:
        raise ObjectNotFound()

    return obj


@router.put("/{lesson_id}", status_code=201)
async def put_lesson(
    lesson_id: int, data: UpdateLesson, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewLesson:
    obj = await lesson_repository.update_lesson(lesson_id, data)
    return obj


@router.get("/{lesson_id}/tasks")
async def get_tasks_for_lesson(
    lesson_id: int, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> list[ViewTask]:
    return await lesson_repository.read_all_tasks_for_lesson(lesson_id)


@router.put("/{lesson_id}/tasks", status_code=201)
async def put_tasks_for_lesson(
    lesson_id: int, task_ids: list[int], lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> None:
    await lesson_repository.set_tasks_for_lesson(lesson_id, task_ids)


# ----------------- Task -----------------


@router.post("/tasks/", status_code=201)
async def post_task(
    data: CreateTask, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewTask:
    obj = await lesson_repository.create_task(data)
    return obj


@router.get("/tasks/{task_id}")
async def get_one_task(
    task_id: int, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewTask:
    return await lesson_repository.read_task(task_id)


@router.put("/tasks/{task_id}", status_code=201)
async def put_task(
    task_id: int, data: UpdateTask, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewTask:
    obj = await lesson_repository.update_task(task_id, data)
    return obj


class RewardEntry(BaseModel):
    reward_id: int
    count: int = 1


@router.put("/tasks/{task_id}/rewards", status_code=201)
async def put_task_rewards(
    task_id: int, rewards: list[RewardEntry], lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewTask:
    await lesson_repository.set_rewards_for_task(task_id, [(r.reward_id, r.count) for r in rewards])
    return await lesson_repository.read_task(task_id)

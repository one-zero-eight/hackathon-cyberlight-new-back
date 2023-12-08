__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel

from src.api.dependencies import DEPENDS_LESSON_REPOSITORY, DEPENDS_VERIFIED_REQUEST
from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult
from src.modules.lesson.repository import LessonRepository
from src.modules.lesson.schemas import ViewLesson, CreateLesson, Answer, ViewTask, CreateTask, UpdateLesson, UpdateTask

router = APIRouter(prefix="/lessons", tags=["Lesson"])


class TaskSolveResult(BaseModel):
    success: bool
    rewards: list[int]


@router.post("/solve")
async def solve(
    answer: Answer, verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST]
) -> TaskSolveResult:
    raise NotImplementedError()


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

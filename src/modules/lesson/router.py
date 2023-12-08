__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel

from src.api.dependencies import DEPENDS_LESSON_REPOSITORY, DEPENDS_VERIFIED_REQUEST
from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult
from src.modules.lesson.repository import LessonRepository
from src.modules.lesson.schemas import ViewLesson, CreateLesson, Answer, ViewTask, CreateTask

router = APIRouter(prefix="/lessons", tags=["Lesson"])


class TaskSolveResult(BaseModel):
    success: bool
    rewards: list[int]


@router.post("/solve")
async def post_task_solve(
    answer: Answer, verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST]
) -> TaskSolveResult:
    raise NotImplementedError()


@router.get("/", response_model=list[ViewLesson])
async def get_all(lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]) -> list[ViewLesson]:
    return await lesson_repository.read_all_lessons()


@router.get("/{lesson_id}")
async def get_one(
    lesson_id: int, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewLesson:
    obj = await lesson_repository.read_lesson(lesson_id)

    if obj is None:
        raise ObjectNotFound()

    return obj


@router.get("/tasks/{task_id}")
async def get_task(task_id: int, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]) -> ViewTask:
    return await lesson_repository.read_task(task_id)


@router.post("/tasks/", status_code=201)
async def post_task(
    data: CreateTask, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewTask:
    obj = await lesson_repository.create_task(data)
    return obj


@router.post("/", status_code=201)
async def post_lesson(
    data: CreateLesson, lesson_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY]
) -> ViewLesson:
    obj = await lesson_repository.create_lesson(data)
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

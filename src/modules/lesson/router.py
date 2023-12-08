__all__ = ["router"]

from fastapi import APIRouter
from pydantic import BaseModel

from src.modules.lesson.schemas import ViewLesson, CreateLesson, Answer, ViewTask, CreateTask

router = APIRouter(prefix="/lessons", tags=["lesson"])


@router.get("/", response_model=list[ViewLesson])
async def get_all() -> list[ViewLesson]:
    raise NotImplementedError()


@router.get("/{test_id}")
async def get_one(test_id: int) -> ViewLesson:
    raise NotImplementedError()


class TestSolveResult(BaseModel):
    is_success: bool
    reward: int


@router.post("/tasks/{task_id}/solve")
async def post_task_solve(task_id: int, answer: Answer) -> TestSolveResult:
    raise NotImplementedError()


@router.get("/tasks/{task_id}")
async def get_task(task_id: int) -> ViewTask:
    raise NotImplementedError()


@router.post("/tasks/", status_code=201)
async def post_task(_: CreateTask) -> ViewTask:
    raise NotImplementedError()


@router.post("/", status_code=201)
async def post_test(_: CreateLesson) -> ViewLesson:
    raise NotImplementedError()

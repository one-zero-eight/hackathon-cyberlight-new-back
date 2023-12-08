__all__ = ["router"]

from fastapi import APIRouter
from src.modules.test.schemas import ViewTest, CreateTest, Answer, ViewTask, CreateTask

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.get("/", response_model=list[ViewTest])
async def get_all() -> list[ViewTest]:
    raise NotImplementedError()


@router.get("/{test_id}")
async def get_one(test_id: int) -> ViewTest:
    raise NotImplementedError()


@router.post("/tasks/{task_id}/solve")
async def post_task_solve(task_id: int, answer: Answer) -> bool:
    raise NotImplementedError()


@router.get("/tasks/{task_id}")
async def get_task(task_id: int) -> ViewTask:
    raise NotImplementedError()


@router.post("/tasks/", status_code=201)
async def post_task(_: CreateTask) -> ViewTask:
    raise NotImplementedError()


@router.post("/", status_code=201)
async def post_test(_: CreateTest) -> ViewTest:
    raise NotImplementedError()

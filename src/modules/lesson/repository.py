__all__ = ["TestRepository"]

from typing import Optional

from src.modules.lesson.schemas import ViewLesson, CreateLesson, CreateTask, ViewTask, UpdateTest
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.models.lesson import Lesson, Task, TaskAssociation
from src.storages.sqlalchemy.utils import *


class TestRepository(SQLAlchemyRepository):
    # ----------------- Test -----------------
    async def create_test(self, data: CreateLesson) -> ViewLesson:
        async with self._create_session() as session:
            q = insert(Lesson).values(data.model_dump()).returning(Lesson)
            obj = await session.scalar(q)
            await session.commit()
            return ViewLesson.model_validate(obj)

    async def read_all_tests(self) -> list[ViewLesson]:
        async with self._create_session() as session:
            q = select(Lesson)
            objs = await session.scalars(q)
            return [ViewLesson.model_validate(obj) for obj in objs]

    async def read_test(self, id_: int) -> Optional[ViewLesson]:
        async with self._create_session() as session:
            q = select(Lesson).where(Lesson.id == id_)
            obj = await session.scalar(q)
            if obj:
                return ViewLesson.model_validate(obj)

    async def update_test(self, id_: int, data: UpdateTest) -> ViewLesson:
        async with self._create_session() as session:
            q = (
                update(Lesson)
                .where(Lesson.id == id_)
                .values(data.model_dump(exclude_none=True, exclude_unset=True))
                .returning(Lesson)
            )
            obj = await session.scalar(q)
            await session.commit()
            return ViewLesson.model_validate(obj)

    async def set_tasks_for_test(self, test_id: int, task_ids: list[int]) -> None:
        async with self._create_session() as session:
            q = delete(TaskAssociation).where(TaskAssociation.test_id == test_id)
            await session.execute(q)
            for i, task_id in enumerate(task_ids):
                q = insert(TaskAssociation).values(test_id=test_id, task_id=task_id, order=i)
                await session.execute(q)
            await session.commit()

    # ----------------- Task -----------------
    async def create_task(self, data: CreateTask) -> ViewTask:
        async with self._create_session() as session:
            q = insert(Task).values(data.model_dump()).returning(Task)
            obj = await session.scalar(q)
            await session.commit()
            return ViewTask.model_validate(obj)

    async def read_all_tasks(self) -> list[ViewTask]:
        async with self._create_session() as session:
            q = select(Task)
            objs = await session.scalars(q)
            return [ViewTask.model_validate(obj) for obj in objs]

    async def read_task(self, id_: int) -> Optional[ViewTask]:
        async with self._create_session() as session:
            q = select(Task).where(Task.id == id_)
            obj = await session.scalar(q)
            if obj:
                return ViewTask.model_validate(obj)

    async def update_task(self, id_: int, data: CreateTask) -> ViewTask:
        async with self._create_session() as session:
            q = (
                update(Task)
                .where(Task.id == id_)
                .values(data.model_dump(exclude_none=True, exclude_unset=True))
                .returning(Task)
            )
            obj = await session.scalar(q)
            await session.commit()
            return ViewTask.model_validate(obj)

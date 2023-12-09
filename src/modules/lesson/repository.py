__all__ = ["LessonRepository"]

from typing import Optional

from src.modules.lesson.schemas import ViewLesson, CreateLesson, CreateTask, ViewTask, UpdateLesson, UpdateTask
from src.storages.sqlalchemy.models import UserTaskAnswer
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.models.lesson import Lesson, Task, TaskAssociation, TaskReward
from src.storages.sqlalchemy.utils import *


class LessonRepository(SQLAlchemyRepository):
    # ----------------- Test -----------------
    async def create_lesson(self, data: CreateLesson) -> ViewLesson:
        async with self._create_session() as session:
            q = insert(Lesson).values(data.model_dump()).returning(Lesson)
            obj = await session.scalar(q)
            await session.commit()
            return ViewLesson.model_validate(obj)

    async def read_all_lessons(self) -> list[ViewLesson]:
        async with self._create_session() as session:
            q = select(Lesson)
            objs = await session.scalars(q)
            return [ViewLesson.model_validate(obj) for obj in objs]

    async def read_lesson(self, id_: int) -> Optional[ViewLesson]:
        async with self._create_session() as session:
            q = select(Lesson).where(Lesson.id == id_)
            obj = await session.scalar(q)
            if obj:
                return ViewLesson.model_validate(obj)

    async def update_lesson(self, id_: int, data: UpdateLesson) -> ViewLesson:
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

    async def upsert_lesson(self, data: CreateLesson) -> ViewLesson:
        async with self._create_session() as session:
            # alias
            q = select(Lesson).where(Lesson.alias == data.alias)
            obj = await session.scalar(q)
            if obj:
                q = (
                    update(Lesson)
                    .where(Lesson.id == obj.id)
                    .values(data.model_dump(exclude_none=True, exclude_unset=True))
                    .returning(Lesson)
                )
                obj = await session.scalar(q)
            else:
                q = insert(Lesson).values(data.model_dump()).returning(Lesson)
                obj = await session.scalar(q)
            await session.commit()
            return ViewLesson.model_validate(obj)

    async def set_tasks_for_lesson(self, test_id: int, task_ids: list[int]) -> None:
        async with self._create_session() as session:
            q = delete(TaskAssociation).where(TaskAssociation.test_id == test_id)
            await session.execute(q)
            for i, task_id in enumerate(task_ids):
                q = insert(TaskAssociation).values(test_id=test_id, task_id=task_id, order=i)
                await session.execute(q)
            await session.commit()

    async def set_tasks_for_lesson_by_aliases(self, lesson_alias: str, task_aliases: list[str]) -> None:
        async with self._create_session() as session:
            q = select(Lesson).where(Lesson.alias == lesson_alias)
            lesson = await session.scalar(q)
            if not lesson:
                return
            q = delete(TaskAssociation).where(TaskAssociation.test_id == lesson.id)
            await session.execute(q)
            for i, task_alias in enumerate(task_aliases):
                q = select(Task).where(Task.alias == task_alias)
                task = await session.scalar(q)
                if not task:
                    continue
                q = insert(TaskAssociation).values(test_id=lesson.id, task_id=task.id, order=i)
                await session.execute(q)
            await session.commit()

    async def get_all_tasks_for_lesson(self, lesson_id: int) -> list[ViewTask]:
        async with self._create_session() as session:
            q = (
                select(Task)
                .join(TaskAssociation, TaskAssociation.task_id == Task.id)
                .where(TaskAssociation.test_id == lesson_id)
                .order_by(TaskAssociation.order)
            )
            objs = await session.scalars(q)
            return [ViewTask.model_validate(obj) for obj in objs]

    async def get_solved_tasks_for_lesson(self, user_id: int, lesson_id: int) -> list[ViewTask]:
        async with self._create_session() as session:
            q = (
                select(Task)
                .join(TaskAssociation, TaskAssociation.task_id == Task.id)
                .join(UserTaskAnswer, UserTaskAnswer.task_id == Task.id)
                .where(UserTaskAnswer.user_id == user_id)
                .where(TaskAssociation.test_id == lesson_id)
                .where(UserTaskAnswer.is_correct)
                .order_by(TaskAssociation.order)
            )
            objs = await session.scalars(q)
            return [ViewTask.model_validate(obj) for obj in objs]

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

    async def read_task_by_alias(self, alias: str) -> Optional[ViewTask]:
        async with self._create_session() as session:
            q = select(Task).where(Task.alias == alias)
            obj = await session.scalar(q)
            if obj:
                return ViewTask.model_validate(obj)

    async def update_task(self, id_: int, data: UpdateTask) -> ViewTask:
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

    async def upsert_task(self, data: CreateTask) -> ViewTask:
        async with self._create_session() as session:
            # alias
            q = select(Task).where(Task.alias == data.alias)
            obj = await session.scalar(q)
            if obj:
                q = (
                    update(Task)
                    .where(Task.id == obj.id)
                    .values(data.model_dump(exclude_none=True, exclude_unset=True))
                    .returning(Task)
                )
                obj = await session.scalar(q)
            else:
                q = insert(Task).values(data.model_dump(exclude_none=True, exclude_unset=True)).returning(Task)
                obj = await session.scalar(q)
            await session.commit()
            return ViewTask.model_validate(obj)

    async def set_rewards_for_task(self, task_id: int, rewards: list[tuple[int, int]]):
        async with self._create_session() as session:
            q = delete(TaskReward).where(TaskReward.task_id == task_id)
            await session.execute(q)
            for i, (reward_id, count) in enumerate(rewards):
                q = insert(TaskReward).values(task_id=task_id, reward_id=reward_id, count=count)
                await session.execute(q)
            await session.commit()

    async def set_rewards_for_task_by_aliases(self, alias: str, rewards: list[tuple[int, int]]):
        async with self._create_session() as session:
            q = select(Task).where(Task.alias == alias)
            task = await session.scalar(q)
            if not task:
                return
            q = delete(TaskReward).where(TaskReward.task_id == task.id)
            await session.execute(q)
            for i, (reward_id, count) in enumerate(rewards):
                q = insert(TaskReward).values(task_id=task.id, reward_id=reward_id, count=count)
                await session.execute(q)
            await session.commit()

    async def read_lesson_by_alias(self, alias: str) -> ViewLesson:
        async with self._create_session() as session:
            q = select(Lesson).where(Lesson.alias == alias)
            obj = await session.scalar(q)
            if obj:
                return ViewLesson.model_validate(obj)

    async def is_solved_task(self, user_id: int, task_id) -> bool:
        async with self._create_session() as session:
            q = select(UserTaskAnswer).where(
                and_(
                    UserTaskAnswer.user_id == user_id,
                    UserTaskAnswer.task_id == task_id,
                    UserTaskAnswer.is_correct,
                )
            )
            obj = await session.scalar(q)
            if obj:
                return True
            return False

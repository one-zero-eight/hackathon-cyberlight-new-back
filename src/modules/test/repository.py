__all__ = ["TestRepository"]

from typing import Optional

from src.modules.test.schemas import ViewTest, CreateTest
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.models.test import Test
from src.storages.sqlalchemy.utils import *


class TestRepository(SQLAlchemyRepository):
    async def create(self, data: CreateTest) -> ViewTest:
        async with self._create_session() as session:
            q = insert(Test).values(data.model_dump()).returning(Test)
            obj = await session.scalar(q)
            await session.commit()
            return ViewTest.model_validate(obj)

    async def read(self, id_: int) -> Optional[ViewTest]:
        async with self._create_session() as session:
            q = select(Test).where(Test.id == id_)
            obj = await session.scalar(q)
            if obj:
                return ViewTest.model_validate(obj)

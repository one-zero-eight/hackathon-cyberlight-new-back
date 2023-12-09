from src.config import settings
from src.modules.report.schemas import UserReport
from src.storages.sqlalchemy import SQLAlchemyStorage
from src.storages.sqlalchemy.utils import *


async def get_rows() -> list[UserReport]:
    async with SQLAlchemyStorage(settings.database.get_async_engine()).create_session() as session:
        q = text(
            """select personal_account.user_id, personal_account.total_exp, users.name from personal_account inner join users on personal_account.user_id=users.id"""
        )
        objs = await session.execute(q)
        if objs:
            return [UserReport.model_validate(obj) for obj in objs]

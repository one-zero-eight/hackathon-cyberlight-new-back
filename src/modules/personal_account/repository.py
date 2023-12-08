from typing import Optional

from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult
from src.storages.sqlalchemy.models import PersonalAccount
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.utils import *
from src.modules.personal_account.schemas import ViewPersonalAccount


class PersonalAccountRepository(SQLAlchemyRepository):
    async def create(self, session, user_id: int) -> None:
        q = insert(PersonalAccount).values(user_id=user_id)
        await session.execute(q)

    async def read(self, verification: VerificationResult) -> Optional[ViewPersonalAccount]:
        async with self._create_session() as session:
            q = select(PersonalAccount).where(PersonalAccount.user_id == verification.user_id)
            obj = await session.scalar(q)
            print(obj)
            if obj:
                return ViewPersonalAccount.model_validate(obj)
            raise ObjectNotFound()

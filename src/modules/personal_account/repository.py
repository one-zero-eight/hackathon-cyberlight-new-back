from typing import Optional

from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult
from src.storages.sqlalchemy.models import PersonalAccount, Reward, PersonalAccountRewards
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.utils import *
from src.modules.personal_account.schemas import (
    ViewPersonalAccount,
    ViewReward,
    CreateReward,
    CreatePersonalAccountReward,
)


class PersonalAccountRepository(SQLAlchemyRepository):
    async def create(self, session, user_id: int) -> None:
        q = insert(PersonalAccount).values(user_id=user_id)
        await session.execute(q)

    async def read(self, verification: VerificationResult) -> Optional[ViewPersonalAccount]:
        async with self._create_session() as session:
            q = select(PersonalAccount).where(PersonalAccount.user_id == verification.user_id)
            obj = await session.scalar(q)
            if obj:
                return ViewPersonalAccount.model_validate(obj)
            raise ObjectNotFound()


class RewardRepository(SQLAlchemyRepository):
    async def create(self, reward_data: CreateReward) -> ViewReward:
        async with self._create_session() as session:
            q = insert(Reward).values(reward_data.model_dump()).returning(Reward)
            result = await session.execute(q)
            await session.commit()
            return ViewReward.model_validate(result)

    async def read(self, _id: int) -> Optional[ViewReward]:
        async with self._create_session() as session:
            q = select(Reward).where(Reward.id == _id)
            obj = await session.scalar(q)
            if obj:
                return ViewReward.model_validate(obj)
            raise ObjectNotFound()

    async def get_all(self) -> list[ViewReward]:
        async with self._create_session() as session:
            q = select(Reward)
            objs = await session.scalars(q)
            if objs:
                return [ViewReward.model_validate(obj) for obj in objs]
            raise ObjectNotFound()

    async def set_to_personal_account(self, create_personal_account_reward: CreatePersonalAccountReward) -> None:
        async with self._create_session() as session:
            q = insert(PersonalAccountRewards).values(create_personal_account_reward.model_dump())
            await session.execute(q)
            await session.commit()

from typing import Optional

from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult
from src.storages.sqlalchemy.models import (
    PersonalAccount,
    Reward,
    PersonalAccountRewards,
    Achievement,
    PersonalAccountAchievements,
)
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.utils import *
from src.modules.personal_account.schemas import (
    ViewPersonalAccount,
    ViewReward,
    CreateReward,
    CreatePersonalAccountReward,
    ViewAchievement,
    CreateAchievement,
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
            reward = Reward(**reward_data.model_dump())
            session.add(reward)
            await session.commit()
            return ViewReward.model_validate(reward)

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
            q = (
                select(PersonalAccountRewards)
                .where(PersonalAccountRewards.reward_id == create_personal_account_reward.reward_id)
                .where(PersonalAccountRewards.personal_account_id == create_personal_account_reward.personal_account_id)
            )
            result = await session.scalar(q)
            if result:
                result.count += 1
                session.add(result)
            else:
                q = insert(PersonalAccountRewards).values(create_personal_account_reward.model_dump())
                await session.execute(q)
            await session.commit()


class AchievementRepository(SQLAlchemyRepository):
    async def create(self, achievement_data: CreateAchievement) -> ViewAchievement:
        async with self._create_session() as session:
            achievement = Achievement(**achievement_data.model_dump())
            session.add(achievement)
            await session.commit()
            return ViewAchievement.model_validate(achievement)

    async def read(self, _id: int) -> Optional[ViewAchievement]:
        async with self._create_session() as session:
            q = select(Achievement).where(Achievement.id == _id)
            obj = await session.scalar(q)
            if obj:
                return ViewAchievement.model_validate(obj)
            raise ObjectNotFound()

    async def set_to_personal_account(self, create_personal_account_achievement: CreatePersonalAccountReward) -> None:
        async with self._create_session() as session:
            q = insert(PersonalAccountAchievements).values(create_personal_account_achievement.model_dump())
            await session.execute(q)
            await session.commit()

    async def get_all(self) -> list[ViewAchievement]:
        async with self._create_session() as session:
            q = select(Achievement)
            objs = await session.scalars(q)
            if objs:
                return [ViewAchievement.model_validate(obj) for obj in objs]
            raise ObjectNotFound()

from typing import Optional

from src.api.exceptions import ObjectNotFound
from src.modules.auth.schemas import VerificationResult

from src.storages.sqlalchemy.models import (
    PersonalAccount,
    Reward,
    PersonalAccountRewards,
    Achievement,
    PersonalAccountAchievements,
    Level,
    BattlePass,
    PersonalAccountBattlePasses,
    LevelRewards,
)
from src.storages.sqlalchemy.models.event import Event, EventParticipants
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.utils import *
from src.modules.personal_account.schemas import (
    ViewPersonalAccount,
    ViewReward,
    CreateReward,
    CreatePersonalAccountReward,
    ViewAchievement,
    CreateAchievement,
    ViewLevel,
    CreateLevel,
    ViewBattlePass,
    CreateBattlePass,
    CreatePersonalAccountBattlePasses,
    UpdateReward,
    UpdateAchievement,
    CreatePersonalAccountAchievement,
    ViewLeaderBoard,
    ViewAchievementWithSummary,
    ViewPersonalAccountBattlePass,
    CreateEvent,
    ViewEvent,
    CreateEventParticipant,
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

    async def increase_exp(self, user_id: int, exp: int) -> None:
        async with self._create_session() as session:
            q = (
                update(PersonalAccount)
                .where(PersonalAccount.user_id == user_id)
                .values(total_exp=PersonalAccount.total_exp + exp)
            )
            await session.execute(q)
            await session.commit()

    async def set_experience(self, user_id: int, exp: int) -> None:
        async with self._create_session() as session:
            q = update(PersonalAccount).where(PersonalAccount.user_id == user_id).values(total_exp=exp)
            await session.execute(q)
            await session.commit()

    async def read_leaderboard(self) -> list[ViewLeaderBoard]:
        async with self._create_session() as session:
            q = text(
                """select personal_account.total_exp, users.name, users.id from personal_account inner join users on personal_account.user_id=users.id order by personal_account.total_exp desc;"""
            )
            objs = await session.execute(q)
            if objs:
                return [ViewLeaderBoard.model_validate(obj) for obj in objs]

    async def read_my_battle_pass(self, verification: VerificationResult) -> ViewPersonalAccountBattlePass:
        async with self._create_session() as session:
            q = (
                select(PersonalAccountBattlePasses)
                .join(BattlePass)
                .filter(
                    and_(
                        BattlePass.is_active,
                        PersonalAccountBattlePasses.personal_account_id == verification.user_id,
                    )
                )
                .limit(1)
            )
            obj = await session.scalar(q)
            if obj is not None:
                return ViewPersonalAccountBattlePass.model_validate(obj)
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

    async def update(self, _id, reward_data: UpdateReward) -> ViewReward:
        async with self._create_session() as session:
            q = (
                update(Reward)
                .where(Reward.id == _id)
                .values(reward_data.model_dump(exclude_none=True, exclude_unset=True))
                .returning(Reward)
            )
            obj = await session.scalar(q)
            await session.commit()
            return ViewReward.model_validate(obj)

    async def get_all(self) -> list[ViewReward]:
        async with self._create_session() as session:
            q = select(Reward)
            objs = await session.scalars(q)
            if objs:
                return [ViewReward.model_validate(obj) for obj in objs]

    async def add_to_personal_account(self, create_personal_account_reward: CreatePersonalAccountReward) -> None:
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

    async def add_rewards_to_personal_account(self, user_id: int, rewards: list[tuple[int, int]]) -> None:
        async with self._create_session() as session:
            q = select(PersonalAccount).where(PersonalAccount.user_id == user_id)
            personal_account = await session.scalar(q)
            if personal_account:
                for reward_id, count in rewards:
                    q = (
                        select(PersonalAccountRewards)
                        .where(PersonalAccountRewards.reward_id == reward_id)
                        .where(PersonalAccountRewards.personal_account_id == personal_account.user_id)
                    )
                    result = await session.scalar(q)
                    if result:
                        result.count += count
                        session.add(result)
                    else:
                        q = insert(PersonalAccountRewards).values(
                            reward_id=reward_id, personal_account_id=personal_account.user_id, count=count
                        )
                        await session.execute(q)
                await session.commit()

    async def set_rewards_to_level(self, level_id: int, rewards: list[int]) -> None:
        async with self._create_session() as session:
            q = delete(LevelRewards).where(LevelRewards.level_id == level_id)
            await session.execute(q)
            for reward_id in rewards:
                q = insert(LevelRewards).values(level_id=level_id, reward_id=reward_id)
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

    async def update(self, _id: int, achievement_data: UpdateAchievement) -> ViewAchievement:
        async with self._create_session() as session:
            q = (
                update(Achievement)
                .where(Achievement.id == _id)
                .values(achievement_data.model_dump(exclude_none=True, exclude_unset=True))
                .returning(Achievement)
            )
            obj = await session.scalar(q)
            await session.commit()
            return ViewAchievement.model_validate(obj)

    async def set_to_personal_account(
        self, create_personal_account_achievement: CreatePersonalAccountAchievement
    ) -> None:
        async with self._create_session() as session:
            # check for exist
            q = (
                select(PersonalAccountAchievements)
                .where(PersonalAccountAchievements.achievement_id == create_personal_account_achievement.achievement_id)
                .where(
                    PersonalAccountAchievements.personal_account_id
                    == create_personal_account_achievement.personal_account_id
                )
            )
            result = await session.scalar(q)
            if result:
                return
            q = insert(PersonalAccountAchievements).values(create_personal_account_achievement.model_dump())
            await session.execute(q)
            await session.commit()

    async def get_all(self) -> list[ViewAchievementWithSummary]:
        async with self._create_session() as session:
            q = select(Achievement)
            objs = await session.scalars(q)
            if objs:
                achievements = [ViewAchievement.model_validate(achievement) for achievement in objs]

                achievement_counts = {}
                for achievement in achievements:
                    q = (
                        select(func.count(PersonalAccountAchievements.personal_account_id))
                        .select_from(PersonalAccountAchievements)
                        .where(PersonalAccountAchievements.achievement_id == achievement.id)
                    )
                    achievement_counts[achievement.id] = await session.scalar(q)
                total_user_count = await session.scalar(select(func.count(PersonalAccount.user_id)))

                achievement_percentages = {}
                for achievement_id, count in achievement_counts.items():
                    achievement_percentages[achievement_id] = count / total_user_count

                achievement_summaries = [
                    ViewAchievementWithSummary(
                        percent=achievement_percentages[achievement.id],
                        total_count=achievement_counts[achievement.id],
                        achievement=achievement,
                    )
                    for achievement in achievements
                ]

                return achievement_summaries


class LevelRepository(SQLAlchemyRepository):
    async def create(self, level_data: CreateLevel) -> ViewLevel:
        async with self._create_session() as session:
            obj = Level(**level_data.model_dump())
            session.add(obj)
            await session.commit()
            q = select(Level).where(Level.id == obj.id)
            level = await session.scalar(q)
            return ViewLevel.model_validate(level)

    async def read(self, _id: int) -> Optional[ViewLevel]:
        async with self._create_session() as session:
            q = select(Level).where(Level.id == _id)
            obj = await session.scalar(q)
            if obj:
                return ViewLevel.model_validate(obj)

    async def get_all(self) -> list[ViewLevel]:
        async with self._create_session() as session:
            q = select(Level)
            objs = await session.scalars(q)
            if objs:
                return [ViewLevel.model_validate(obj) for obj in objs]


class BattlePassRepository(SQLAlchemyRepository):
    async def create(self, battle_pass_data: CreateBattlePass, id_: Optional[int] = None) -> ViewBattlePass:
        async with self._create_session() as session:
            dct = battle_pass_data.model_dump()
            if id_ is not None:
                dct["id"] = id_
            obj = BattlePass(**dct)
            session.add(obj)
            await session.commit()
            q = select(BattlePass).where(BattlePass.id == obj.id)
            battle_pass = await session.scalar(q)
            return ViewBattlePass.model_validate(battle_pass)

    async def read(self, _id: int) -> Optional[ViewBattlePass]:
        async with self._create_session() as session:
            q = select(BattlePass).where(BattlePass.id == _id)
            obj = await session.scalar(q)
            if obj:
                return ViewBattlePass.model_validate(obj)

    async def delete(self, _id: int) -> None:
        async with self._create_session() as session:
            q = delete(BattlePass).where(BattlePass.id == _id)
            await session.execute(q)
            await session.commit()

    async def get_all(self) -> list[ViewBattlePass]:
        async with self._create_session() as session:
            q = select(BattlePass)
            objs = await session.scalars(q)
            if objs:
                return [ViewBattlePass.model_validate(obj) for obj in objs]

    async def add_to_user(self, create_personal_account_bp: CreatePersonalAccountBattlePasses) -> None:
        async with self._create_session() as session:
            q = select(PersonalAccountBattlePasses).where(
                and_(
                    PersonalAccountBattlePasses.personal_account_id == create_personal_account_bp.personal_account_id,
                    PersonalAccountBattlePasses.battle_pass_id == create_personal_account_bp.battle_pass_id,
                )
            )
            result = await session.scalar(q)

            if not result:
                pa_bp = PersonalAccountBattlePasses(**create_personal_account_bp.model_dump())
                session.add(pa_bp)
            await session.commit()

    async def increase_battle_exp(self, user_id: int, exp: int) -> None:
        async with self._create_session() as session:
            # select
            q = (
                select(PersonalAccountBattlePasses)
                .join(BattlePass)
                .where(
                    and_(
                        BattlePass.is_active,
                        PersonalAccountBattlePasses.personal_account_id == user_id,
                    )
                )
            )

            passes = await session.scalars(q)

            if passes:
                for pa_bp in passes:
                    # update
                    q = (
                        update(PersonalAccountBattlePasses)
                        .where(
                            and_(
                                PersonalAccountBattlePasses.personal_account_id == user_id,
                                PersonalAccountBattlePasses.battle_pass_id == pa_bp.battle_pass_id,
                            )
                        )
                        .values(experience=PersonalAccountBattlePasses.experience + exp)
                    )
                    await session.execute(q)

                await session.commit()


class EventRepository(SQLAlchemyRepository):
    async def create(self, event_data: CreateEvent) -> ViewEvent:
        async with self._create_session() as session:
            obj = Event(**event_data.model_dump())
            session.add(obj)
            await session.commit()
            q = select(Event).where(Event.id == obj.id)
            event = await session.scalar(q)
            return ViewEvent.model_validate(event)

    async def read(self, _id: int) -> Optional[ViewEvent]:
        async with self._create_session() as session:
            q = select(Event).where(Event.id == _id)
            obj = await session.scalar(q)
            if obj:
                return ViewEvent.model_validate(obj)

    async def get_active(self) -> Optional[ViewEvent]:
        async with self._create_session() as session:
            q = select(Event).where(Event.is_active)
            obj = await session.scalar(q)
            if obj:
                return ViewEvent.model_validate(obj)

    async def add_participant_to_event(self, event_participant: CreateEventParticipant) -> None:
        async with self._create_session() as session:
            obj = EventParticipants(**event_participant.model_dump())
            session.add(obj)
            await session.commit()

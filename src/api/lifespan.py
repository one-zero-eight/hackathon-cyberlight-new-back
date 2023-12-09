__all__ = ["lifespan"]

from contextlib import asynccontextmanager
from pathlib import Path

import jinja2
from fastapi import FastAPI

from src.api.dependencies import Dependencies
from src.config import settings
from src.config_schema import Environment
from src.modules.auth.repository import AuthRepository
from src.modules.consultation.repository import ConsultationRepository
from src.modules.consultation.schemas import CreateTimeslot, CreateConsultant
from src.modules.lesson.repository import LessonRepository
from src.modules.lesson.schemas import CreateLesson, CreateTask
from src.modules.personal_account.schemas import (
    UpdateReward,
    UpdateAchievement,
    CreatePersonalAccountAchievement,
    CreateBattlePass,
    CreateLevel,
    CreatePersonalAccountBattlePasses,
)
from src.modules.phishing.repository import PhishingRepository
from src.modules.smtp.repository import SMTPRepository
from src.modules.user.repository import UserRepository
from src.modules.personal_account.repository import (
    PersonalAccountRepository,
    RewardRepository,
    AchievementRepository,
    LevelRepository,
    BattlePassRepository,
)
from src.storages.predefined.storage import Predefined

from src.storages.sqlalchemy.storage import SQLAlchemyStorage


async def setup_repositories():
    # ------------------- Repositories Dependencies -------------------
    storage = SQLAlchemyStorage(settings.database.get_async_engine())
    user_repository = UserRepository(storage)
    auth_repository = AuthRepository(storage)
    reward_repository = RewardRepository(storage)
    personal_account_repository = PersonalAccountRepository(storage)
    lesson_repository = LessonRepository(storage)
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(settings.static_files.directory),
        autoescape=True,
    )
    smtp_repository = SMTPRepository()
    achievement_repository = AchievementRepository(storage)
    level_repository = LevelRepository(storage)
    battle_pass_repository = BattlePassRepository(storage)
    consultation_repository = ConsultationRepository(storage)
    phishing_repository = PhishingRepository()

    Dependencies.set_auth_repository(auth_repository)
    Dependencies.set_storage(storage)
    Dependencies.set_user_repository(user_repository)
    Dependencies.set_personal_account_repository(personal_account_repository)
    Dependencies.set_lesson_repository(lesson_repository)
    Dependencies.set_achievement_repository(achievement_repository)
    Dependencies.set_reward_repository(reward_repository)
    Dependencies.set_jinja2_env(jinja2_env)
    Dependencies.set_smtp_repository(smtp_repository)
    Dependencies.set_level_repository(level_repository)
    Dependencies.set_battle_pass_repository(battle_pass_repository)
    Dependencies.set_consultation_repository(consultation_repository)
    Dependencies.set_phishing_repository(phishing_repository)

    if settings.environment == Environment.DEVELOPMENT:
        import logging

        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.info("SQLAlchemy logging is enabled!")


def setup_admin_panel(app: FastAPI):
    from src.modules.admin.app import init_app

    init_app(app, settings.database.get_async_engine())


async def setup_predefined():
    user_repository = Dependencies.get_user_repository()

    superuser = await user_repository.read_by_login(settings.predefined.first_superuser_login)
    if not superuser:
        superuser = await user_repository.create_superuser(
            login=settings.predefined.first_superuser_login,
            password=settings.predefined.first_superuser_password,
            email=settings.predefined.first_superuser_email,
        )

    predefined: Predefined = Predefined.from_yaml(Path("predefined.yaml"))
    lesson_repository = Dependencies.get_lesson_repository()
    reward_repository = Dependencies.get_reward_repository()
    achievement_repository = Dependencies.get_achievement_repository()
    consultation_repository = Dependencies.get_consultation_repository()
    battle_pass_repository = Dependencies.get_battle_pass_repository()
    level_repository = Dependencies.get_level_repository()
    for consultant in predefined.consultants:
        db_consultant = await consultation_repository.read_consultant(consultant.id)
        if not db_consultant:
            await consultation_repository.create_consultant(
                CreateConsultant.model_validate(consultant, from_attributes=True), consultant_id=consultant.id
            )

        await consultation_repository.set_timeslots(
            consultant.id,
            [CreateTimeslot.model_validate(timeslot, from_attributes=True) for timeslot in consultant.timeslots],
        )

    for reward in predefined.rewards:
        db_reward = await reward_repository.read(reward.id)
        if not db_reward:
            await reward_repository.create(reward)
        else:
            await reward_repository.update(reward.id, UpdateReward.model_validate(reward, from_attributes=True))

    for achievement in predefined.achievements:
        db_achievement = await achievement_repository.read(achievement.id)
        if not db_achievement:
            await achievement_repository.create(achievement)
        else:
            await achievement_repository.update(
                achievement.id, UpdateAchievement.model_validate(achievement, from_attributes=True)
            )
        await achievement_repository.set_to_personal_account(
            CreatePersonalAccountAchievement(
                achievement_id=achievement.id,
                personal_account_id=superuser.id,
            )
        )

    for task in predefined.tasks:
        await lesson_repository.upsert_task(CreateTask.model_validate(task, from_attributes=True))
        await lesson_repository.set_rewards_for_task_by_aliases(
            task.alias, [(entry.reward_id, entry.count) for entry in task.rewards]
        )

    for lesson in predefined.lessons:
        await lesson_repository.upsert_lesson(CreateLesson.model_validate(lesson, from_attributes=True))
        await lesson_repository.set_tasks_for_lesson_by_aliases(
            lesson.alias, [task_alias for task_alias in lesson.tasks]
        )

    for battlepass in predefined.battle_passes:
        db_battlepass = await battle_pass_repository.read(battlepass.id)
        if not db_battlepass:
            await battle_pass_repository.create(
                id_=battlepass.id, battle_pass_data=CreateBattlePass.model_validate(battlepass, from_attributes=True)
            )
            for level in battlepass.levels:
                db_level = await level_repository.create(
                    CreateLevel(
                        battle_pass_id=battlepass.id,
                        experience=level.experience,
                        value=level.value,
                    )
                )
                await reward_repository.set_rewards_to_level(db_level.id, [reward_id for reward_id in level.rewards])
        await battle_pass_repository.add_to_user(
            CreatePersonalAccountBattlePasses(
                battle_pass_id=battlepass.id,
                personal_account_id=superuser.id,
            )
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup

    await setup_repositories()
    await setup_predefined()

    setup_admin_panel(app)

    yield

    # Application shutdown
    from src.api.dependencies import Dependencies

    storage = Dependencies.get_storage()
    await storage.close_connection()

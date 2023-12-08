__all__ = ["lifespan"]

from contextlib import asynccontextmanager
from pathlib import Path

import jinja2
from fastapi import FastAPI

from src.api.dependencies import Dependencies
from src.config import settings
from src.config_schema import Environment
from src.modules.auth.repository import AuthRepository
from src.modules.lesson.repository import LessonRepository
from src.modules.lesson.schemas import CreateLesson
from src.modules.smtp.repository import SMTPRepository
from src.modules.user.repository import UserRepository
from src.modules.personal_account.repository import PersonalAccountRepository, RewardRepository, AchievementRepository
from src.storages.predefined.lessons import PredefinedLessons

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

    Dependencies.set_auth_repository(auth_repository)
    Dependencies.set_storage(storage)
    Dependencies.set_user_repository(user_repository)
    Dependencies.set_personal_account_repository(personal_account_repository)
    Dependencies.set_lesson_repository(lesson_repository)
    Dependencies.set_achievement_repository(achievement_repository)
    Dependencies.set_reward_repository(reward_repository)
    Dependencies.set_jinja2_env(jinja2_env)
    Dependencies.set_smtp_repository(smtp_repository)

    if settings.environment == Environment.DEVELOPMENT:
        import logging

        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.info("SQLAlchemy logging is enabled!")


def setup_admin_panel(app: FastAPI):
    from src.modules.admin.app import init_app

    init_app(app, settings.database.get_async_engine())


async def setup_predefined():
    user_repository = Dependencies.get_user_repository()
    if not await user_repository.read_by_login(settings.predefined.first_superuser_login):
        await user_repository.create_superuser(
            login=settings.predefined.first_superuser_login,
            password=settings.predefined.first_superuser_password,
        )

    predefined: PredefinedLessons = PredefinedLessons.from_yaml(Path("predefined.yaml"))
    lesson_repository = Dependencies.get_lesson_repository()
    for lesson in predefined.lessons:
        await lesson_repository.upsert_lesson(CreateLesson.model_validate(lesson, from_attributes=True))
    for task in predefined.tasks:
        await lesson_repository.upsert_task(task)

    for lesson in predefined.lessons:
        await lesson_repository.set_tasks_for_lesson_by_aliases(
            lesson.alias, [task_alias for task_alias in lesson.tasks]
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

"""

Live Template for dependencies:
    enum(
        "storage: Annotated[SQLAlchemyStorage, DEPENDS_STORAGE]",
        "user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY]",
        "auth_repository: Annotated[AuthRepository, DEPENDS_AUTH_REPOSITORY]",
        "verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST]",
    )
"""

from fastapi import Depends

from typing import TYPE_CHECKING

from jinja2 import Environment

if TYPE_CHECKING:
    from src.modules.user.repository import UserRepository
    from src.modules.auth.repository import AuthRepository
    from src.modules.personal_account.repository import (
        PersonalAccountRepository,
        RewardRepository,
        AchievementRepository,
        LevelRepository,
        BattlePassRepository,
    )
    from src.modules.lesson.repository import LessonRepository
    from src.storages.sqlalchemy.storage import SQLAlchemyStorage
    from src.modules.smtp.repository import SMTPRepository
    from src.modules.consultation.repository import ConsultationRepository


class Dependencies:
    _storage: "SQLAlchemyStorage"
    _user_repository: "UserRepository"
    _auth_repository: "AuthRepository"
    _personal_account_repository: "PersonalAccountRepository"
    _reward_repository: "RewardRepository"
    _lesson_repository: "LessonRepository"
    _jinja2_env: "Environment"
    _smtp_repository: "SMTPRepository"
    _achievement_repository: "AchievementRepository"
    _level_repository: "LevelRepository"
    _battle_pass_repository: "BattlePassRepository"
    _consultation_repository: "ConsultationRepository"

    @classmethod
    def get_storage(cls) -> "SQLAlchemyStorage":
        return cls._storage

    @classmethod
    def set_storage(cls, storage: "SQLAlchemyStorage"):
        cls._storage = storage

    @classmethod
    def get_user_repository(cls) -> "UserRepository":
        return cls._user_repository

    @classmethod
    def set_user_repository(cls, user_repository: "UserRepository"):
        cls._user_repository = user_repository

    @classmethod
    def get_auth_repository(cls) -> "AuthRepository":
        return cls._auth_repository

    @classmethod
    def set_auth_repository(cls, auth_repository: "AuthRepository"):
        cls._auth_repository = auth_repository

    @classmethod
    def get_reward_repository(cls) -> "RewardRepository":
        return cls._reward_repository

    @classmethod
    def set_reward_repository(cls, reward_repository: "RewardRepository"):
        cls._reward_repository = reward_repository

    @classmethod
    def get_personal_account_repository(cls) -> "PersonalAccountRepository":
        return cls._personal_account_repository

    @classmethod
    def set_personal_account_repository(cls, personal_account_repository: "PersonalAccountRepository"):
        cls._personal_account_repository = personal_account_repository

    @classmethod
    def get_lesson_repository(cls) -> "LessonRepository":
        return cls._lesson_repository

    @classmethod
    def set_lesson_repository(cls, lesson_repository: "LessonRepository"):
        cls._lesson_repository = lesson_repository

    @classmethod
    def get_achievement_repository(cls) -> "AchievementRepository":
        return cls._achievement_repository

    @classmethod
    def set_achievement_repository(cls, achievement_repository: "AchievementRepository"):
        cls._achievement_repository = achievement_repository

    @classmethod
    def get_jinja2_env(cls) -> "Environment":
        return cls._jinja2_env

    @classmethod
    def set_jinja2_env(cls, jinja2_env: "Environment"):
        cls._jinja2_env = jinja2_env

    @classmethod
    def get_smtp_repository(cls) -> "SMTPRepository":
        return cls._smtp_repository

    @classmethod
    def set_smtp_repository(cls, smtp_repository: "SMTPRepository"):
        cls._smtp_repository = smtp_repository

    @classmethod
    def get_level_repository(cls) -> "LevelRepository":
        return cls._level_repository

    @classmethod
    def set_level_repository(cls, level_repository: "LevelRepository"):
        cls._level_repository = level_repository

    @classmethod
    def get_battle_pass_repository(cls) -> "BattlePassRepository":
        return cls._battle_pass_repository

    @classmethod
    def set_battle_pass_repository(cls, battle_pass_repository: "BattlePassRepository"):
        cls._battle_pass_repository = battle_pass_repository

    @classmethod
    def set_consultation_repository(cls, consultation_repository):
        cls._consultation_repository = consultation_repository

    @classmethod
    def get_consultation_repository(cls) -> "ConsultationRepository":
        return cls._consultation_repository


DEPENDS = Depends(lambda: Dependencies)
"""It's a dependency injection container for FastAPI.
See `FastAPI docs <(https://fastapi.tiangolo.com/tutorial/dependencies/)>`_ for more info"""
DEPENDS_STORAGE = Depends(Dependencies.get_storage)
DEPENDS_USER_REPOSITORY = Depends(Dependencies.get_user_repository)
DEPENDS_AUTH_REPOSITORY = Depends(Dependencies.get_auth_repository)
DEPENDS_PERSONAL_ACCOUNT_REPOSITORY = Depends(Dependencies.get_personal_account_repository)
DEPENDS_REWARD_REPOSITORY = Depends(Dependencies.get_reward_repository)
DEPENDS_LESSON_REPOSITORY = Depends(Dependencies.get_lesson_repository)
DEPENDS_SMTP_REPOSITORY = Depends(Dependencies.get_smtp_repository)
DEPENDS_ACHIEVEMENT_REPOSITORY = Depends(Dependencies.get_achievement_repository)
DEPENDS_LEVEL_REPOSITORY = Depends(Dependencies.get_level_repository)
DEPENDS_BATTLE_PASS_REPOSITORY = Depends(Dependencies.get_battle_pass_repository)
DEPENDS_CONSULTATION_REPOSITORY = Depends(Dependencies.get_consultation_repository)

from src.modules.auth.dependencies import verify_request  # noqa: E402

DEPENDS_VERIFIED_REQUEST = Depends(verify_request)

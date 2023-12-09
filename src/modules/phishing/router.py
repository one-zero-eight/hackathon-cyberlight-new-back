__all__ = ["router"]

import datetime
import random
from time import sleep
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from starlette.responses import PlainTextResponse

from src.api.dependencies import (
    Dependencies,
    DEPENDS_PERSONAL_ACCOUNT_REPOSITORY,
    DEPENDS_REWARD_REPOSITORY,
    DEPENDS_LESSON_REPOSITORY,
    DEPENDS_VERIFIED_REQUEST,
    DEPENDS_BATTLE_PASS_REPOSITORY,
    DEPENDS_ACHIEVEMENT_REPOSITORY,
    DEPENDS_SMTP_REPOSITORY,
    DEPENDS_USER_REPOSITORY,
)
from src.api.exceptions import ObjectNotFound
from src.config import settings
from src.modules.auth.schemas import VerificationResult
from src.modules.lesson.repository import LessonRepository
from src.modules.lesson.router import TaskSolveResult
from src.modules.personal_account.repository import (
    PersonalAccountRepository,
    RewardRepository,
    BattlePassRepository,
    AchievementRepository,
)
from src.modules.personal_account.schemas import CreatePersonalAccountAchievement
from src.modules.smtp.repository import SMTPRepository
from src.modules.user.repository import UserRepository

router = APIRouter(prefix="", tags=["Phishing"])


@router.get("/phishing-callback/{messageId}", response_class=PlainTextResponse)
async def phishing_callback(
    messageId: str,
) -> str:
    phishing_repo = Dependencies.get_phishing_repository()

    phish = phishing_repo.get_phishing(messageId)

    if phish is not None:
        return "Что-то не так...."

    raise ObjectNotFound()


@router.get("/finish-phishing/")
async def finish_phishing_task(
    phishing_url: str,
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    achievement_repository: Annotated[AchievementRepository, DEPENDS_ACHIEVEMENT_REPOSITORY],
    personal_account: Annotated[PersonalAccountRepository, DEPENDS_PERSONAL_ACCOUNT_REPOSITORY],
    battle_pass_repository: Annotated[BattlePassRepository, DEPENDS_BATTLE_PASS_REPOSITORY],
    reward_repository: Annotated[RewardRepository, DEPENDS_REWARD_REPOSITORY],
    task_repository: Annotated[LessonRepository, DEPENDS_LESSON_REPOSITORY],
) -> TaskSolveResult:
    _, _, messageId = phishing_url.rpartition("/")
    phishing_repo = Dependencies.get_phishing_repository()
    phish = phishing_repo.pop_phishing(messageId)

    if phish is not None:
        phish_task = await task_repository.read_task_by_alias("phishing")
        await personal_account.increase_exp(verification.user_id, phish_task.exp)
        await battle_pass_repository.increase_battle_exp(verification.user_id, phish_task.exp)
        rewards = [(ass.reward.id, ass.count) for ass in phish_task.rewards_associations]
        await reward_repository.add_rewards_to_personal_account(verification.user_id, rewards)
        await achievement_repository.set_to_personal_account(
            CreatePersonalAccountAchievement(
                personal_account_id=verification.user_id,
                achievement_id=100000007,
            )
        )
        return TaskSolveResult(success=True, rewards=phish_task.rewards, exp=phish_task.exp)

    return TaskSolveResult(success=False)


@router.get("/start-phishing-task/")
async def start_phishing_task(
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    smtp_repository: Annotated[SMTPRepository, DEPENDS_SMTP_REPOSITORY],
    background_tasks: BackgroundTasks,
):
    phishing_repo = Dependencies.get_phishing_repository()
    message_id = _generate_message_id()
    user = await user_repository.read(verification.user_id)
    # random value from 5 minutes to 60 minutes
    when_to_send = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(5, 60))
    when_to_send: datetime.datetime
    phishing_repo.add_phishing(
        user_id=verification.user_id, email=user.email, message_id=message_id, when_to_send=when_to_send
    )

    message = smtp_repository.render_message(settings.smtp.phishing_template, user.email, message_id=message_id)

    background_tasks.add_task(
        delayed_message,
        message,
        user.email,
        when_to_send,
    )


def delayed_message(
    message: str,
    to: str,
    when_to_send: datetime.datetime,
):
    while datetime.datetime.now() < when_to_send:
        sleep(10)
    smtp_repository = Dependencies.get_smtp_repository()
    smtp_repository.send(message, to)


def _generate_message_id() -> str:
    message_id = "%030x" % random.randrange(16**30)
    return message_id

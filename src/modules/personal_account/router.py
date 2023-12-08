__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import (
    DEPENDS_PERSONAL_ACCOUNT_REPOSITORY,
    DEPENDS_REWARD_REPOSITORY,
    DEPENDS_ACHIEVEMENT_REPOSITORY,
    DEPENDS_BATTLE_PASS_REPOSITORY,
)
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.personal_account.repository import (
    PersonalAccountRepository,
    RewardRepository,
    AchievementRepository,
    BattlePassRepository,
)
from src.modules.personal_account.schemas import (
    ViewPersonalAccount,
    ViewReward,
    CreateReward,
    CreatePersonalAccountReward,
    ViewAchievement,
    CreateAchievement,
    CreatePersonalAccountAchievement,
    ViewBattlePass,
    CreateBattlePass,
    CreatePersonalAccountBattlePasses,
)

router = APIRouter(tags=["Personal Account"])


@router.get(
    "/personal_account/",
    responses={
        200: {"description": "My personal account"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_my_personal_account(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    personal_account_repository: Annotated[PersonalAccountRepository, DEPENDS_PERSONAL_ACCOUNT_REPOSITORY],
) -> ViewPersonalAccount:
    personal_account = await personal_account_repository.read(verification)
    return personal_account


@router.get(
    "/rewards/",
    responses={
        200: {"description": "Get all rewards"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_all_rewards(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    reward_repository: Annotated[RewardRepository, DEPENDS_REWARD_REPOSITORY],
) -> list[ViewReward]:
    all_rewards = await reward_repository.get_all()
    return all_rewards


@router.get(
    "/reward/{reward_id}",
    responses={
        200: {"description": "Read reward by id"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def read_reward(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    reward_repository: Annotated[RewardRepository, DEPENDS_REWARD_REPOSITORY],
    reward_id: int,
) -> ViewReward:
    reward = await reward_repository.read(reward_id)
    return reward


@router.post(
    "/reward/",
    responses={
        200: {"description": "Create reward"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def create_reward(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    reward_repository: Annotated[RewardRepository, DEPENDS_REWARD_REPOSITORY],
    obj: CreateReward,
) -> ViewReward:
    reward = await reward_repository.create(obj)
    return reward


@router.post(
    "/reward/set-to-personal-account",
    responses={
        200: {"description": "Set reward to personal account"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def set_reward_to_personal_account(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    reward_repository: Annotated[RewardRepository, DEPENDS_REWARD_REPOSITORY],
    obj: CreatePersonalAccountReward,
):
    await reward_repository.add_to_personal_account(obj)
    return {"success": True}


@router.get(
    "/achievements/",
    responses={
        200: {"description": "Get all achievements"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_all_achievements(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    achievement_repository: Annotated[AchievementRepository, DEPENDS_ACHIEVEMENT_REPOSITORY],
) -> list[ViewAchievement]:
    all_achievements = await achievement_repository.get_all()
    return all_achievements


@router.get(
    "/achievement/{achievement_id}",
    responses={
        200: {"description": "Read achievement by id"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def read_achievement(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    achievement_repository: Annotated[AchievementRepository, DEPENDS_ACHIEVEMENT_REPOSITORY],
    achievement_id: int,
) -> ViewAchievement:
    achievement = await achievement_repository.read(achievement_id)
    return achievement


@router.post(
    "/achievement/",
    responses={
        200: {"description": "Create achievement"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def create_achievement(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    achievement_repository: Annotated[AchievementRepository, DEPENDS_ACHIEVEMENT_REPOSITORY],
    obj: CreateAchievement,
) -> ViewAchievement:
    achievement = await achievement_repository.create(obj)
    return achievement


@router.post(
    "/achievement/set-to-personal-account",
    responses={
        200: {"description": "Set achievement to personal account"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def set_achievement_to_personal_account(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    achievement_repository: Annotated[AchievementRepository, DEPENDS_ACHIEVEMENT_REPOSITORY],
    obj: CreatePersonalAccountAchievement,
) -> None:
    await achievement_repository.set_to_personal_account(obj)
    return {"success": True}


@router.get(
    "/battle-passes/",
    responses={
        200: {"description": "Get all battle-passes"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_all_battle_passes(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    battle_pass_repository: Annotated[BattlePassRepository, DEPENDS_BATTLE_PASS_REPOSITORY],
) -> list[ViewBattlePass]:
    battle_passes = await battle_pass_repository.get_all()
    return battle_passes


@router.get(
    "/battle-pass/{battle_pass_id}",
    responses={
        200: {"description": "Read battle pass by id"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def read_battle_pass(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    battle_pass_repository: Annotated[BattlePassRepository, DEPENDS_BATTLE_PASS_REPOSITORY],
    battle_pass_id: int,
) -> ViewBattlePass:
    battle_pass = await battle_pass_repository.read(battle_pass_id)
    return battle_pass


@router.post(
    "/battle-pass/",
    responses={
        200: {"description": "Create battle-pass"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def create_battle_pass(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    battle_pass_repository: Annotated[BattlePassRepository, DEPENDS_BATTLE_PASS_REPOSITORY],
    obj: CreateBattlePass,
) -> ViewBattlePass:
    battle_pass = await battle_pass_repository.create(obj)
    return battle_pass


@router.post(
    "/battle-pass/set-to-user",
    responses={
        200: {"description": "Set battle pass to user"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def set_battle_pass_to_user(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    battle_pass_repository: Annotated[BattlePassRepository, DEPENDS_BATTLE_PASS_REPOSITORY],
    obj: CreatePersonalAccountBattlePasses,
) -> None:
    await battle_pass_repository.set_to_user(obj)
    return {"success": True}

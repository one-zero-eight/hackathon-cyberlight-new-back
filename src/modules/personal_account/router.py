__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import DEPENDS_PERSONAL_ACCOUNT_REPOSITORY, DEPENDS_REWARD_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.personal_account.repository import PersonalAccountRepository, RewardRepository
from src.modules.personal_account.schemas import (
    ViewPersonalAccount,
    ViewReward,
    CreateReward,
    CreatePersonalAccountReward,
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
async def get_my(
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
async def get_all(
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
) -> None:
    await reward_repository.set_to_personal_account(obj)
    return {"success": True}

__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter

from src.api.dependencies import DEPENDS_USER_REPOSITORY, DEPENDS_VERIFIED_REQUEST
from src.api.exceptions import (
    IncorrectCredentialsException,
    NoCredentialsException,
    ForbiddenException,
)
from src.modules.auth.schemas import VerificationResult
from src.modules.user.repository import UserRepository
from src.modules.user.schemas import ViewUser, CreateUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    responses={
        200: {"description": "User info"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_me(
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
) -> ViewUser:
    """
    Get user info
    """

    user = await user_repository.read(verification.user_id)
    user: ViewUser
    return user


@router.post(
    "/",
)
async def create_user(
    create_user: CreateUser,
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
) -> ViewUser:
    """
    Create user
    """

    user = await user_repository.read(verification.user_id)
    if not user.is_admin:
        raise ForbiddenException()

    new_user = await user_repository.create(create_user)
    return new_user


@router.get("/")
async def get_users(
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
) -> list[ViewUser]:
    """
    Get users
    """

    user = await user_repository.read(verification.user_id)
    if not user.is_admin:
        raise ForbiddenException()

    users = await user_repository.read_all()
    return users

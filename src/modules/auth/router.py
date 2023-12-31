__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DEPENDS_AUTH_REPOSITORY, DEPENDS_USER_REPOSITORY, Dependencies
from src.modules.auth.repository import TokenRepository, AuthRepository
from src.modules.auth.schemas import AuthResult, AuthCredentials
from src.modules.personal_account.schemas import CreatePersonalAccountAchievement, CreatePersonalAccountBattlePasses
from src.modules.user.repository import UserRepository
from src.modules.user.schemas import CreateUser

router = APIRouter(prefix="/auth", tags=["Auth"])


# by-tag
@router.post("/by-credentials", response_model=AuthResult)
async def by_credentials(
    credentials: AuthCredentials, auth_repository: Annotated[AuthRepository, DEPENDS_AUTH_REPOSITORY]
):
    user_id = await auth_repository.authenticate_user(password=credentials.password, login=credentials.login)
    token = TokenRepository.create_access_token(user_id)
    return AuthResult(token=token, success=True)


@router.post("/start-registration")
async def start_registration(
    user: CreateUser,
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    auth_repository: Annotated[AuthRepository, DEPENDS_AUTH_REPOSITORY],
):
    db_user = await user_repository.read_by_login(user.login)
    db_user = db_user or await user_repository.read_by_email(user.email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    auth_repository.start_registration(user)


@router.post("/finish-registration")
async def finish_registration(
    email: str,
    code: str,
    auth_repository: Annotated[AuthRepository, DEPENDS_AUTH_REPOSITORY],
):
    user = await auth_repository.finish_registration(email, code)
    token = TokenRepository.create_access_token(user.id)

    if user.name == "":
        achievement_repository = Dependencies.get_achievement_repository()
        await achievement_repository.set_to_personal_account(
            CreatePersonalAccountAchievement(
                achievement_id=100000001,  # anonym
                personal_account_id=user.id,
            )
        )

    battle_pass_repository = Dependencies.get_battle_pass_repository()

    await battle_pass_repository.add_to_user(
        CreatePersonalAccountBattlePasses(
            battle_pass_id=101,
            personal_account_id=user.id,
        )
    )

    return AuthResult(token=token, success=True)

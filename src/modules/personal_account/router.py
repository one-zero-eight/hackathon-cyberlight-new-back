__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import DEPENDS_PERSONAL_ACCOUNT_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.personal_account.repository import PersonalAccountRepository
from src.modules.personal_account.schemas import ViewPersonalAccount

router = APIRouter(prefix="/personal_account", tags=["Personal Account"])


@router.get(
    "/",
    responses={
        200: {"description": "My personal account"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
    response_model=ViewPersonalAccount,
)
async def get_my(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    personal_account_repository: Annotated[PersonalAccountRepository, DEPENDS_PERSONAL_ACCOUNT_REPOSITORY],
) -> ViewPersonalAccount:
    personal_account = await personal_account_repository.read(verification)
    return personal_account

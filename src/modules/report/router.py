import csv
import json
from typing import Annotated
from io import StringIO

from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from starlette.responses import Response

from src.api.dependencies import DEPENDS_USER_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException, ForbiddenException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.report.schemas import UserReport
from src.modules.report.utils import get_rows
from src.modules.user.repository import UserRepository

router = APIRouter(prefix="/report", tags=["Report"])


@router.get(
    "/",
    responses={
        200: {"description": "Export report", "media_type": "text/csv"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
    response_class=FileResponse,
)
async def get_report(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
) -> Response:
    user = await user_repository.read(verification.user_id)
    if not user.is_admin:
        raise ForbiddenException()

    rows = await get_rows()
    fieldnames = list(UserReport.model_json_schema()["properties"].keys())
    out = StringIO()
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(json.loads(UserReport(**row.model_dump()).model_dump_json()))
    return Response(content=out.getvalue(), media_type="text/csv")

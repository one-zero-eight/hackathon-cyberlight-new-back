__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter

from src.api.dependencies import DEPENDS_VERIFIED_REQUEST, DEPENDS_CONSULTATION_REPOSITORY, DEPENDS_USER_REPOSITORY
from src.api.exceptions import ForbiddenException
from src.modules.auth.schemas import VerificationResult
from src.modules.consultation.repository import ConsultationRepository
from src.modules.consultation.schemas import ViewConsultant, CreateConsultant, CreateTimeslot, AddAppointment
from src.modules.user.repository import UserRepository

router = APIRouter(prefix="/consultation", tags=["Consultation"])


@router.post("/consultants/", status_code=201)
async def post_consultant(
    data: CreateConsultant,
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    consultation_repository: Annotated["ConsultationRepository", DEPENDS_CONSULTATION_REPOSITORY],
) -> ViewConsultant:
    user = await user_repository.read(verification.user_id)
    if not user.is_admin:
        raise ForbiddenException()
    return await consultation_repository.create_consultant(data)


@router.get("/consultants/")
async def get_all_consultants(
    consultation_repository: Annotated["ConsultationRepository", DEPENDS_CONSULTATION_REPOSITORY]
) -> list[ViewConsultant]:
    return await consultation_repository.read_all_consultants()


@router.get("/consultants/{consultant_id}")
async def get_consultant(
    consultant_id: int, consultation_repository: Annotated["ConsultationRepository", DEPENDS_CONSULTATION_REPOSITORY]
) -> ViewConsultant:
    return await consultation_repository.read_consultant(consultant_id)


@router.post("/consultants/{consultant_id}/timeslots/", status_code=201)
async def add_timeslot(
    consultant_id: int,
    data: CreateTimeslot,
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    consultation_repository: Annotated["ConsultationRepository", DEPENDS_CONSULTATION_REPOSITORY],
) -> ViewConsultant:
    user = await user_repository.read(verification.user_id)
    if not user.is_admin:
        raise ForbiddenException()
    return await consultation_repository.add_timeslot(consultant_id, data)


@router.delete("/consultants/{consultant_id}/timeslots/{timeslot_id}")
async def remove_timeslot(
    consultant_id: int,
    timeslot_id: int,
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    consultation_repository: Annotated["ConsultationRepository", DEPENDS_CONSULTATION_REPOSITORY],
) -> ViewConsultant:
    user = await user_repository.read(verification.user_id)
    if not user.is_admin:
        raise ForbiddenException()
    return await consultation_repository.remove_timeslot(consultant_id, timeslot_id)


@router.post("/consultants/{consultant_id}/appointments/", status_code=201)
async def add_appointment(
    appointment: AddAppointment,
    verification: Annotated[VerificationResult, DEPENDS_VERIFIED_REQUEST],
    consultation_repository: Annotated["ConsultationRepository", DEPENDS_CONSULTATION_REPOSITORY],
) -> ViewConsultant:
    return await consultation_repository.add_appointment(
        consultant_id=verification.user_id, user_id=verification.user_id, appointment=appointment
    )

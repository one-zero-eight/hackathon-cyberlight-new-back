__all__ = ["ConsultationRepository"]

from typing import Optional

from src.modules.consultation.schemas import ViewConsultant, CreateConsultant, CreateTimeslot, AddAppointment
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.models.consultation import Consultant, Timeslot, Appointment
from src.storages.sqlalchemy.utils import *


class ConsultationRepository(SQLAlchemyRepository):
    async def create_consultant(self, data: CreateConsultant, consultant_id: Optional[int] = None) -> ViewConsultant:
        async with self._create_session() as session:
            dct = data.model_dump()
            if consultant_id is not None:
                dct["id"] = consultant_id
            q = insert(Consultant).values(dct).returning(Consultant)
            obj = await session.scalar(q)
            await session.commit()
            return ViewConsultant.model_validate(obj)

    async def read_all_consultants(self) -> list[ViewConsultant]:
        async with self._create_session() as session:
            q = select(Consultant)
            objs = await session.scalars(q)
            return [ViewConsultant.model_validate(obj) for obj in objs]

    async def read_consultant(self, id_: int) -> Optional[ViewConsultant]:
        async with self._create_session() as session:
            q = select(Consultant).where(Consultant.id == id_)
            obj = await session.scalar(q)
            if obj:
                return ViewConsultant.model_validate(obj)

    async def add_timeslot(self, consultant_id: int, data: CreateTimeslot) -> ViewConsultant:
        async with self._create_session() as session:
            q = insert(Timeslot).values(**data.model_dump(), consultant_id=consultant_id).returning(Timeslot)
            obj = await session.scalar(q)
            await session.commit()
            return ViewConsultant.model_validate(obj)

    async def remove_timeslot(self, consultant_id: int, timeslot_id: int) -> ViewConsultant:
        async with self._create_session() as session:
            q = delete(Timeslot).where(Timeslot.id == timeslot_id)
            await session.execute(q)
            await session.commit()
            q = select(Consultant).where(Consultant.id == consultant_id)
            obj = await session.scalar(q)
            return ViewConsultant.model_validate(obj)

    async def set_timeslots(self, consultant_id: int, timeslots: list[CreateTimeslot]) -> ViewConsultant:
        async with self._create_session() as session:
            q = delete(Timeslot).where(Timeslot.consultant_id == consultant_id)
            await session.execute(q)
            for timeslot in timeslots:
                q = insert(Timeslot).values(**timeslot.model_dump(), consultant_id=consultant_id).returning(Timeslot)
                await session.scalar(q)
            await session.commit()
            q = select(Consultant).where(Consultant.id == consultant_id)
            obj = await session.scalar(q)
            return ViewConsultant.model_validate(obj)

    async def add_appointment(self, consultant_id: int, user_id: int, appointment: AddAppointment) -> ViewConsultant:
        async with self._create_session() as session:
            q = (
                insert(Appointment)
                .values(**appointment.model_dump(), consultant_id=consultant_id, user_id=user_id)
                .returning(Appointment)
            )
            obj = await session.scalar(q)
            await session.commit()
            return ViewConsultant.model_validate(obj)

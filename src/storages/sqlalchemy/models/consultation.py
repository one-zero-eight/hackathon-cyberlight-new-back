import datetime

from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.utils import *


class Consultant(Base, IdMixin):
    __tablename__ = "consultants"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default="")
    image: Mapped[str] = mapped_column(nullable=True)
    timeslots: Mapped[list["Timeslot"]] = relationship("Timeslot", back_populates="consultant", lazy="selectin")
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="consultant", lazy="selectin"
    )


class Timeslot(Base, IdMixin):
    __tablename__ = "timeslots"

    consultant_id: Mapped[int] = mapped_column(ForeignKey(Consultant.id), nullable=False)
    day: Mapped[int] = mapped_column(nullable=False)
    start: Mapped[str] = mapped_column(nullable=False)
    end: Mapped[str] = mapped_column(nullable=False)
    consultant: Mapped[Consultant] = relationship("Consultant", back_populates="timeslots", viewonly=True)
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="timeslot")


class Appointment(Base, IdMixin):
    __tablename__ = "appointments"

    date: Mapped[datetime.date] = mapped_column(DateTime(timezone=True), nullable=False)
    consultant_id: Mapped[int] = mapped_column(ForeignKey(Consultant.id), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    timeslot_id: Mapped[int] = mapped_column(ForeignKey(Timeslot.id), nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True, default="")
    consultant: Mapped[Consultant] = relationship("Consultant", back_populates="appointments", viewonly=True)
    timeslot: Mapped[Timeslot] = relationship("Timeslot", back_populates="appointments", lazy="joined", viewonly=True)

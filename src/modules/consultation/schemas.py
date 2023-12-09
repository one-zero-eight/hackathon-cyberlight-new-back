import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ViewTimeslot(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Obj id")
    consultant_id: int = Field(..., description="Consultant obj id", examples=[0, 1, 3])
    day: int = Field(..., description="Day of the week (Monday is 0)", examples=[0, 1, 2, 3, 4, 5, 6])
    start: str = Field(..., description="Start time of the timeslot (in minutes)", examples=["10:00"])
    end: str = Field(..., description="Duration of the timeslot (in minutes)", examples=["12:00"])


class ViewAppointment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: datetime.date
    consultant_id: int
    user_id: int
    timeslot: ViewTimeslot
    comment: Optional[str] = Field(None, description="Comment for the appointment", examples=["Как дела?"])


class ViewConsultant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Obj id")
    name: str = Field(..., description="Consultant name (title)", examples=["Анонимус"])
    description: str = Field(..., description="Reward description", examples=["Не дал узнать о себе"])
    image: Optional[str] = Field(
        None, description="Image path", examples=["static/images/consultant_images/consultant_image.png"]
    )
    timeslots: Optional[list[ViewTimeslot]] = Field(
        default_factory=list, description="List of timeslots for the consultant"
    )

    appointments: Optional[list[ViewAppointment]] = Field(
        default_factory=list, description="List of appointments for the consultant"
    )


class CreateTimeslot(BaseModel):
    day: int = Field(..., description="Day of the week (Monday is 0)", examples=[0, 1, 2, 3, 4, 5, 6])
    start: str = Field(..., description="Start time of the timeslot", examples=["10:00"])
    end: str = Field(..., description="Duration of the timeslot", examples=["12:00"])


class AddAppointment(BaseModel):
    date: datetime.date
    timeslot_id: int
    comment: Optional[str] = Field(None, description="Comment for the appointment", examples=["Как дела?"])


class CreateConsultant(BaseModel):
    name: str = Field(..., description="Consultant name (title)", examples=["Анонимус"])
    description: str = Field(..., description="Reward description", examples=["Не дал узнать о себе"])
    image: Optional[str] = Field(
        None, description="Image path", examples=["static/images/consultant_images/consultant_image.png"]
    )

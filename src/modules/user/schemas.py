__all__ = ["ViewUser", "CreateUser"]

from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRoles(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


class ViewUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: Optional[str] = Field(None, description="Email of the user")
    login: str
    name: str
    password_hash: str = Field(exclude=True)
    role: UserRoles = UserRoles.DEFAULT

    @property
    def is_admin(self) -> bool:
        return self.role == UserRoles.ADMIN


class CreateUser(BaseModel):
    login: str
    password: str
    email: str
    name: str

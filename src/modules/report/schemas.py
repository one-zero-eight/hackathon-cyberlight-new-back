from pydantic import BaseModel, ConfigDict, Field


class UserReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., description="User id")
    name: str = Field(..., description="User name")
    total_exp: int = Field(..., description="Total exp")

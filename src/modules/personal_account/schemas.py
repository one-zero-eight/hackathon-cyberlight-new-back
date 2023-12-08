from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from src.storages.sqlalchemy.models.personal_account import RewardType


class ViewPersonalAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., description="Owner User ID", examples=[0])
    rewards: Optional[list["ViewReward"]] = Field(default_factory=list, description="List of rewards")
    achievements: Optional[list["ViewAchievement"]] = Field(default_factory=list, description="List of achievements")
    battle_passes: Optional[list["ViewBattlePass"]] = Field(
        default_factory=list, description="List of battle passes of personal account"
    )


class ViewReward(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Reward name (title)", examples=["Промокод на скидку от партнеров"])
    content: str = Field(..., description="Reward content (useful thing)", examples=["ADASD!#412V"])
    type: "RewardType" = Field(..., description="Type of reward", examples=["default"])
    image: Optional[str] = Field(
        default="", description="Image path", examples=["static/images/reward_images/reward_image.png"]
    )
    icon: Optional[str] = Field(
        default="", description="Icon path", examples=["static/images/reward_icons/reward_icon.png"]
    )


class ViewAchievement(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Achievement name (title)", examples=["Анонимус"])
    description: str = Field(..., description="Reward description", examples=["Не дал узнать о себе"])
    image: Optional[str] = Field(
        default="", description="Image path", examples=["static/images/achievement_images/achievement_image.png"]
    )
    icon: Optional[str] = Field(
        default="", description="Icon path", examples=["static/images/achievement_icons/achievement_icon.png"]
    )


class ViewBattlePass(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    levels: Optional[list["ViewLevel"]] = Field(
        default_factory=list, description="List of levels set to current battle pass"
    )
    is_active: bool = Field(..., description="Is current battle pass active for users", examples=[True, False])


class ViewLevel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    experience: int = Field(
        ..., description="Amount of experience needed to reach this level", examples=[100, 1000, 10000]
    )
    value: int = Field(..., description="Level value: the first, the second...", examples=[1, 2, 3, 4, 5])
    rewards: Optional[list["ViewReward"]] = Field(
        default_factory=list, description="List of rewards for the reaching current level"
    )


class BattlePassExperience(BaseModel):
    experience: int = Field(..., description="Experience of current battle pass", examples=[10, 77, 1882])


ViewPersonalAccount.model_rebuild()
ViewLevel.model_rebuild()
ViewReward.model_rebuild()
ViewBattlePass.model_rebuild()
ViewAchievement.model_rebuild()

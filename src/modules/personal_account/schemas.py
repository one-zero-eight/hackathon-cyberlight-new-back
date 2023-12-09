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
    total_exp: int = Field(..., description="Total experience of personal account", examples=[0, 100, 1000])


class ViewReward(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Obj id")
    name: str = Field(..., description="Reward name (title)", examples=["Промокод на скидку от партнеров"])
    content: str = Field(..., description="Reward content (useful thing)", examples=["ADASD!#412V"])
    type: "RewardType" = Field(..., description="Type of reward", examples=["xp", "none", "item"])
    image: Optional[str] = Field(
        default="", description="Image path", examples=["static/images/reward_images/reward_image.png"]
    )


class ViewAchievement(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Obj id")
    name: str = Field(..., description="Achievement name (title)", examples=["Анонимус"])
    description: str = Field(..., description="Reward description", examples=["Не дал узнать о себе"])
    image: Optional[str] = Field(
        default="", description="Image path", examples=["static/images/achievement_images/achievement_image.png"]
    )


class ViewBattlePass(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Obj id")
    levels: Optional[list["ViewLevel"]] = Field(
        default_factory=list, description="List of levels set to current battle pass"
    )
    is_active: bool = Field(..., description="Is current battle pass active for users", examples=[True, False])


class ViewLevel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Obj id")
    experience: int = Field(
        ..., description="Amount of experience needed to reach this level", examples=[100, 1000, 10000]
    )
    value: int = Field(..., description="Level value: the first, the second...", examples=[1, 2, 3, 4, 5])
    rewards: Optional[list[ViewReward]] = Field(
        default_factory=list, description="List of rewards for the reaching current level"
    )


class CreateReward(BaseModel):
    name: str = Field(..., description="Reward name (title)", examples=["Промокод на скидку от партнеров"])
    content: str = Field(..., description="Reward content (useful thing)", examples=["ADASD!#412V"])
    type: "RewardType" = Field(..., description="Type of reward", examples=["default"])
    image: Optional[str] = Field(
        default="", description="Image path", examples=["static/images/reward_images/reward_image.png"]
    )


class UpdateReward(BaseModel):
    name: Optional[str] = Field(None, description="Reward name (title)", examples=["Промокод на скидку от партнеров"])
    content: Optional[str] = Field(None, description="Reward content (useful thing)", examples=["ADASD!#412V"])
    type: Optional["RewardType"] = Field(None, description="Type of reward", examples=["default"])
    image: Optional[str] = Field(
        None, description="Image path", examples=["static/images/reward_images/reward_image.png"]
    )


class CreatePersonalAccountReward(BaseModel):
    reward_id: int = Field(..., description="Reward obj id", examples=[0, 1, 3])
    personal_account_id: int = Field(..., description="Personal account obj id", examples=[1, 2, 3])


class CreateAchievement(BaseModel):
    name: str = Field(..., description="Achievement name (title)", examples=["Анонимус"])
    description: str = Field(..., description="Reward description", examples=["Не дал узнать о себе"])
    image: Optional[str] = Field(
        default="", description="Image path", examples=["static/images/achievement_images/achievement_image.png"]
    )


class UpdateAchievement(BaseModel):
    name: Optional[str] = Field(None, description="Achievement name (title)", examples=["Анонимус"])
    description: Optional[str] = Field(None, description="Reward description", examples=["Не дал узнать о себе"])
    image: Optional[str] = Field(
        None, description="Image path", examples=["static/images/achievement_images/achievement_image.png"]
    )


class CreatePersonalAccountAchievement(BaseModel):
    achievement_id: int = Field(..., description="Achievement obj id", examples=[0, 1, 3])
    personal_account_id: int = Field(..., description="Personal account obj id", examples=[1, 2, 3])


class CreateBattlePass(BaseModel):
    levels: Optional[list["ViewLevel"]] = Field(
        default_factory=list, description="List of levels set to current battle pass"
    )
    is_active: bool = Field(..., description="Is current battle pass active for users", examples=[True, False])


class CreatePersonalAccountBattlePasses(BaseModel):
    battle_pass_id: int = Field(..., description="Battle Pass ID")
    personal_account_id: int = Field(..., description="Personal Account ID")


class CreateLevel(BaseModel):
    experience: int = Field(
        ..., description="Amount of experience needed to reach this level", examples=[100, 1000, 10000]
    )
    value: int = Field(..., description="Level value: the first, the second...", examples=[1, 2, 3, 4, 5])


class CreateBattlePassLevel(BaseModel):
    battle_pass_id: int = Field(..., description="Battle pass id")
    level_id: int = Field(..., description="Level id")


class BattlePassExperience(BaseModel):
    experience: int = Field(..., description="Experience of current battle pass", examples=[10, 77, 1882])


class ViewLeaderBoard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_exp: int = Field(..., description="Total exp of user")
    name: str = Field(..., description="User name")
    id: int = Field(..., description="User ID")


ViewPersonalAccount.model_rebuild()
ViewReward.model_rebuild()
ViewBattlePass.model_rebuild()
ViewAchievement.model_rebuild()

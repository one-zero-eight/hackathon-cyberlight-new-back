__all__ = ["router"]

from fastapi import APIRouter

from src.config import settings
from src.config_schema import Environment

router = APIRouter(prefix="/dev", tags=["Development"])

if settings.environment == Environment.PRODUCTION:
    raise RuntimeError("You can't use this router in production environment!")

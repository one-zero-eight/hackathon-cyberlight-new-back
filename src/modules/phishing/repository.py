__all__ = ["PhishingRepository"]

import datetime
from typing import Optional

from pydantic import BaseModel


class Phishing(BaseModel):
    user_id: int
    email: str
    message_id: str
    when_to_send: datetime.datetime


class PhishingRepository:
    _phishing: dict[str, Phishing]  # msg_id -> Phishing
    phishing_url = "https://x.innohassle.ru"

    def __init__(self):
        self._phishing = {}

    def add_phishing(self, user_id: int, email: str, message_id: str, when_to_send: datetime.datetime) -> None:
        if message_id in self._phishing:
            return
        self._phishing[message_id] = Phishing(
            user_id=user_id, email=email, message_id=message_id, when_to_send=when_to_send
        )

    def get_phishing(self, message_id: str) -> Optional[Phishing]:
        return self._phishing.get(message_id, None)

    def pop_phishing(self, message_id: str) -> Optional[Phishing]:
        if message_id in self._phishing:
            return self._phishing.pop(message_id)

__all__ = ["TokenRepository", "AuthRepository"]

import random
from datetime import timedelta, datetime
from typing import Optional

from authlib.jose import jwt, JoseError
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select

from src.api.dependencies import Dependencies
from src.api.exceptions import IncorrectCredentialsException
from src.config import settings
from src.modules.auth.schemas import VerificationResult, UserCredentialsFromDB, EmailFlow
from src.modules.user.schemas import CreateUser, ViewUser
from src.storages.sqlalchemy.models import User
from src.storages.sqlalchemy.repository import SQLAlchemyRepository


class TokenRepository:
    ALGORITHM = "RS256"

    @classmethod
    async def verify_access_token(cls, auth_token: str) -> VerificationResult:
        try:
            payload = jwt.decode(auth_token, settings.jwt_public_key)
        except JoseError:
            return VerificationResult(success=False)

        user_repository = Dependencies.get_user_repository()
        user_id: str = payload.get("sub")

        if user_id is None or not user_id.isdigit():
            return VerificationResult(success=False)

        converted_user_id = int(user_id)

        if await user_repository.read(converted_user_id) is None:
            return VerificationResult(success=False)

        return VerificationResult(success=True, user_id=converted_user_id)

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        access_token = TokenRepository._create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(days=1),
        )
        return access_token

    @classmethod
    def _create_access_token(cls, data: dict, expires_delta: timedelta) -> str:
        payload = data.copy()
        issued_at = datetime.utcnow()
        expire = issued_at + expires_delta
        payload.update({"exp": expire, "iat": issued_at})
        encoded_jwt = jwt.encode({"alg": cls.ALGORITHM}, payload, settings.jwt_private_key.get_secret_value())
        return str(encoded_jwt, "utf-8")


class AuthRepository(SQLAlchemyRepository):
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"])
    _flows: dict[str, EmailFlow]  # email -> flow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._flows = {}

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD_CONTEXT.hash(password)

    async def authenticate_user(self, login: str, password: str) -> int:
        user_credentials = await self._get_user(login)
        if user_credentials is None:
            raise IncorrectCredentialsException()
        password_verified = await self.verify_password(password, user_credentials.password_hash)
        if not password_verified:
            raise IncorrectCredentialsException()
        return user_credentials.user_id

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    def start_registration(self, user: CreateUser) -> None:
        email = user.email
        code = _generate_auth_code()
        self._flows[email] = EmailFlow(
            user=user,
            code=code,
        )
        smtp = Dependencies.get_smtp_repository()
        message = smtp.render_message(settings.smtp.mailing_template, email, code=code)
        smtp.send(message, email)

    async def finish_registration(self, email: str, code: str) -> ViewUser:
        flow = self._flows.get(email)
        if flow is None:
            raise IncorrectCredentialsException()
        if flow.code != code:
            raise IncorrectCredentialsException()

        user_repository = Dependencies.get_user_repository()

        db_user = await user_repository.read_by_login(flow.user.login)
        db_user = db_user or await user_repository.read_by_email(flow.user.email)

        if db_user is not None:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = await user_repository.create(flow.user)
        self._flows.pop(email)
        return new_user

    async def _get_user(self, login: str) -> Optional[UserCredentialsFromDB]:
        async with self._create_session() as session:
            q = select(User.id, User.password_hash).where(User.login == login)
            user = (await session.execute(q)).one_or_none()
            if user:
                return UserCredentialsFromDB(
                    user_id=user.id,
                    password_hash=user.password_hash,
                )


def _generate_auth_code() -> str:
    # return random 6-digit code
    return str(random.randint(100_000, 999_999))

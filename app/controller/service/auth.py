from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from app.controller.service.user import UserService
from app.core.settings import settings
from app.domain.model.user import UserModel
from app.domain.schema.auth import LoginRequest


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self._service: UserService = user_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def login(self, data: LoginRequest) -> dict[str, str]:
        user = await self.authenticate_user(data=data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=settings.app.security.access_token_expire_minutes
        )
        access_token = await self.create_access_token(
            data={"sub": user.email, "scope": "credentials", "roles": []},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def logout(self, email: str) -> UserModel | HTTPException:
        return await self._service.get_by_email(email=email)

    async def authenticate_user(self, data: LoginRequest) -> bool | UserModel:
        user = await self._service.get_by_email(email=data.username)
        if not user:
            return False
        if not self._service.verify_password(data.password, user.password):
            return False
        return user

    async def create_access_token(
            self, data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.app.security.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.app.security.secret_key,
            algorithm=settings.app.security.algorithm,
        )
        return encoded_jwt

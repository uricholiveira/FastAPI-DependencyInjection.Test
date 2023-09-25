from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

from app.controller.repository.user import UserRepository
from app.domain.model.user import UserModel
from app.domain.schema.user import UserSchema


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_one(self) -> UserModel:
        return self._repository.get()

    async def get_by_email(self, email: str) -> UserModel | HTTPException:
        user = self._repository.get(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def create(self, data: UserSchema) -> UserModel:
        user = UserModel()
        user.name = data.name
        user.email = data.email
        user.password = self.get_password_hash(password=data.password)

        return self._repository.create(user=user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

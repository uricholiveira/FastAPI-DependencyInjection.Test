from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.domain.model.user import UserModel


class UserRepository:
    def __init__(
            self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get(self, email: str = None) -> UserModel | None:
        with self.session_factory() as session:
            query = session.query(UserModel)
            if email is not None:
                query = query.filter_by(email=email)
            return query.first()

    def create(self, user: UserModel) -> UserModel:
        with self.session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

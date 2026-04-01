import uuid

from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    def create_user(self, name: str, email: str) -> User:
        self._raise_if_email_already_taken(email)
        user = User(id=str(uuid.uuid4()), name=name, email=email)
        self._repository.save(user)
        return user

    def get_user(self, user_id: str) -> User:
        user = self._repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user



    def _raise_if_email_already_taken(self, email: str) -> None:
        existing = self._repository.find_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email)

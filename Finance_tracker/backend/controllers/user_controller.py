from backend.models.user import User
from backend.services.user_service import UserService


class UserController:
    def __init__(self, user_service: UserService):
        self._service = user_service

    def create_user(self, name: str, email: str) -> dict:
        user = self._service.create_user(name, email)
        return self._to_response(user)

    def get_user(self, user_id: str) -> dict:
        user = self._service.get_user(user_id)
        return self._to_response(user)



    def _to_response(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }

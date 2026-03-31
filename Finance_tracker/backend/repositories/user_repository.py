import json
import os
from typing import Optional, List

from backend.models.user import User


class UserRepository:
    def __init__(self, storage_path: str):
        self._storage_path = storage_path
        self._ensure_file_exists()

    def save(self, user: User) -> None:
        all_users = self._load_all()
        all_users[user.id] = self._to_dict(user)
        self._persist(all_users)

    def find_by_id(self, user_id: str) -> Optional[User]:
        all_users = self._load_all()
        data = all_users.get(user_id)
        return self._to_model(data) if data else None

    def find_by_email(self, email: str) -> Optional[User]:
        all_users = self._load_all()
        for data in all_users.values():
            if data["email"] == email:
                return self._to_model(data)
        return None

    def find_all(self) -> List[User]:
        all_users = self._load_all()
        return [self._to_model(data) for data in all_users.values()]



    def _ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        if not os.path.exists(self._storage_path):
            self._persist({})

    def _load_all(self) -> dict:
        with open(self._storage_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _persist(self, data: dict) -> None:
        with open(self._storage_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def _to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }

    def _to_model(self, data: dict) -> User:
        return User(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            created_at=data["created_at"],
        )

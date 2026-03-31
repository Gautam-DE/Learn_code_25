import json
import os
from typing import Optional, List

from backend.models.budget import Budget


class BudgetRepository:
    def __init__(self, storage_path: str):
        self._storage_path = storage_path
        self._ensure_file_exists()

    def save(self, budget: Budget) -> None:
        all_budgets = self._load_all()
        all_budgets[budget.id] = self._to_dict(budget)
        self._persist(all_budgets)

    def find_by_id(self, budget_id: str) -> Optional[Budget]:
        all_budgets = self._load_all()
        data = all_budgets.get(budget_id)
        return self._to_model(data) if data else None

    def find_by_user_category_month(
        self, user_id: str, category: str, month: str
    ) -> Optional[Budget]:
        all_budgets = self._load_all()
        for data in all_budgets.values():
            if self._matches(data, user_id, category, month):
                return self._to_model(data)
        return None

    def find_all_by_user(self, user_id: str) -> List[Budget]:
        all_budgets = self._load_all()
        return [
            self._to_model(data)
            for data in all_budgets.values()
            if data["user_id"] == user_id
        ]



    def _matches(
        self, data: dict, user_id: str, category: str, month: str
    ) -> bool:
        return (
            data["user_id"] == user_id
            and data["category"].lower() == category.lower()
            and data["month"] == month
        )

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

    def _to_dict(self, budget: Budget) -> dict:
        return {
            "id": budget.id,
            "user_id": budget.user_id,
            "category": budget.category,
            "month": budget.month,
            "limit_amount": budget.limit_amount,
            "spent_amount": budget.spent_amount,
        }

    def _to_model(self, data: dict) -> Budget:
        return Budget(
            id=data["id"],
            user_id=data["user_id"],
            category=data["category"],
            month=data["month"],
            limit_amount=data["limit_amount"],
            spent_amount=data["spent_amount"],
        )

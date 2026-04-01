import uuid
from typing import List

from backend.models.budget import Budget
from backend.repositories.budget_repository import BudgetRepository
from backend.exceptions.budget_exceptions import BudgetAlreadyExistsError


class BudgetService:
    def __init__(self, budget_repository: BudgetRepository):
        self._repository = budget_repository

    def set_budget(
        self, user_id: str, category: str, month: str, limit_amount: float
    ) -> Budget:
        self._raise_if_budget_already_set(user_id, category, month)
        budget = Budget(
            id=str(uuid.uuid4()),
            user_id=user_id,
            category=category,
            month=month,
            limit_amount=limit_amount,
        )
        self._repository.save(budget)
        return budget

    def get_budgets(self, user_id: str) -> List[Budget]:
        return self._repository.find_all_by_user(user_id)



    def _raise_if_budget_already_set(
        self, user_id: str, category: str, month: str
    ) -> None:
        existing = self._repository.find_by_user_category_month(
            user_id, category, month
        )
        if existing:
            raise BudgetAlreadyExistsError(category, month)

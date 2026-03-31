from typing import List

from backend.models.budget import Budget
from backend.services.budget_service import BudgetService


class BudgetController:
    def __init__(self, budget_service: BudgetService):
        self._service = budget_service

    def set_budget(
        self, user_id: str, category: str, month: str, limit_amount: float
    ) -> dict:
        budget = self._service.set_budget(user_id, category, month, limit_amount)
        return self._to_response(budget)

    def get_budgets(self, user_id: str) -> List[dict]:
        budgets = self._service.get_budgets(user_id)
        return [self._to_response(b) for b in budgets]



    def _to_response(self, budget: Budget) -> dict:
        return {
            "id": budget.id,
            "category": budget.category,
            "month": budget.month,
            "limit_amount": budget.limit_amount,
            "spent_amount": budget.spent_amount,
            "is_exceeded": budget.is_exceeded(),
            "remaining": budget.remaining_amount(),
        }

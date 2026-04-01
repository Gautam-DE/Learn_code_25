from typing import List

from backend.models.transaction import Transaction, TransactionType
from backend.repositories.transaction_repository import TransactionRepository


class ReportService:
    def __init__(self, transaction_repository: TransactionRepository):
        self._repository = transaction_repository

    def get_monthly_summary(self, user_id: str, month: str) -> dict:
        transactions = self._fetch_transactions_for_month(user_id, month)
        total_income = self._sum_by_type(transactions, TransactionType.INCOME)
        total_expense = self._sum_by_type(transactions, TransactionType.EXPENSE)
        savings = total_income - total_expense

        return {
            "month": month,
            "total_income": total_income,
            "total_expense": total_expense,
            "savings": savings,
            "transaction_count": len(transactions),
        }



    def _fetch_transactions_for_month(
        self, user_id: str, month: str
    ) -> List[Transaction]:
        start_date = f"{month}-01"
        end_date = f"{month}-31"
        return self._repository.find_by_user_and_date_range(
            user_id, start_date, end_date
        )

    def _sum_by_type(
        self, transactions: List[Transaction], transaction_type: TransactionType
    ) -> float:
        return sum(
            t.amount for t in transactions if t.type == transaction_type
        )

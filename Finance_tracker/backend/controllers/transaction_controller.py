from typing import Optional, List

from backend.models.transaction import Transaction
from backend.services.transaction_service import TransactionService


class TransactionController:
    def __init__(self, transaction_service: TransactionService):
        self._service = transaction_service

    def add_transaction(
        self,
        user_id: str,
        transaction_type: str,
        amount: float,
        category: str,
        date: str,
        description: str = "",
    ) -> dict:
        transaction = self._service.add_transaction(
            user_id, transaction_type, amount, category, date, description
        )
        return self._to_response(transaction)

    def get_transactions(
        self,
        user_id: str,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[dict]:
        transactions = self._service.get_transactions(
            user_id, category, start_date, end_date
        )
        return [self._to_response(t) for t in transactions]

    def delete_transaction(self, transaction_id: str) -> dict:
        self._service.delete_transaction(transaction_id)
        return {"message": f"Transaction '{transaction_id}' deleted successfully."}



    def _to_response(self, transaction: Transaction) -> dict:
        return {
            "id": transaction.id,
            "type": transaction.type.value,
            "amount": transaction.amount,
            "category": transaction.category,
            "date": transaction.date,
            "description": transaction.description,
        }

import uuid
from typing import List, Optional

from backend.models.transaction import Transaction, TransactionType
from backend.repositories.transaction_repository import TransactionRepository
from backend.repositories.budget_repository import BudgetRepository
from backend.adapters.notification_port import NotificationPort
from backend.exceptions.transaction_exceptions import (
    TransactionNotFoundError,
    InvalidTransactionTypeError,
    InvalidAmountError,
)


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        budget_repository: BudgetRepository,
        notification_port: NotificationPort,
    ):
        self._transaction_repository = transaction_repository
        self._budget_repository = budget_repository
        self._notification_port = notification_port

    def add_transaction(
        self,
        user_id: str,
        transaction_type: str,
        amount: float,
        category: str,
        date: str,
        description: str = "",
    ) -> Transaction:
        validated_type = self._parse_transaction_type(transaction_type)
        self._validate_amount(amount)

        transaction = Transaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=validated_type,
            amount=amount,
            category=category,
            date=date,
            description=description,
        )
        self._transaction_repository.save(transaction)

        if validated_type == TransactionType.EXPENSE:
            self._update_budget_and_notify_if_exceeded(user_id, category, amount, date)

        return transaction

    def get_transactions(
        self,
        user_id: str,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Transaction]:
        if category:
            return self._transaction_repository.find_by_user_and_category(
                user_id, category
            )
        if start_date and end_date:
            return self._transaction_repository.find_by_user_and_date_range(
                user_id, start_date, end_date
            )
        return self._transaction_repository.find_all_by_user(user_id)

    def delete_transaction(self, transaction_id: str) -> None:
        deleted = self._transaction_repository.delete(transaction_id)
        if not deleted:
            raise TransactionNotFoundError(transaction_id)



    def _parse_transaction_type(self, raw_type: str) -> TransactionType:
        try:
            return TransactionType(raw_type.lower())
        except ValueError:
            raise InvalidTransactionTypeError(raw_type)

    def _validate_amount(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError(amount)

    def _update_budget_and_notify_if_exceeded(
        self, user_id: str, category: str, amount: float, date: str
    ) -> None:
        month = date[:7]
        budget = self._budget_repository.find_by_user_category_month(
            user_id, category, month
        )
        if not budget:
            return

        budget.spent_amount += amount
        self._budget_repository.save(budget)

        if budget.is_exceeded():
            self._notification_port.send_budget_exceeded_alert(
                category, budget.spent_amount, budget.limit_amount
            )

import json
import os
from typing import Optional, List

from backend.models.transaction import Transaction, TransactionType


class TransactionRepository:
    def __init__(self, storage_path: str):
        self._storage_path = storage_path
        self._ensure_file_exists()

    def save(self, transaction: Transaction) -> None:
        all_transactions = self._load_all()
        all_transactions[transaction.id] = self._to_dict(transaction)
        self._persist(all_transactions)

    def delete(self, transaction_id: str) -> bool:
        all_transactions = self._load_all()
        if transaction_id not in all_transactions:
            return False
        del all_transactions[transaction_id]
        self._persist(all_transactions)
        return True

    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        all_transactions = self._load_all()
        data = all_transactions.get(transaction_id)
        return self._to_model(data) if data else None

    def find_all_by_user(self, user_id: str) -> List[Transaction]:
        all_transactions = self._load_all()
        return [
            self._to_model(data)
            for data in all_transactions.values()
            if data["user_id"] == user_id
        ]

    def find_by_user_and_category(
        self, user_id: str, category: str
    ) -> List[Transaction]:
        return [
            t
            for t in self.find_all_by_user(user_id)
            if t.category.lower() == category.lower()
        ]

    def find_by_user_and_date_range(
        self, user_id: str, start_date: str, end_date: str
    ) -> List[Transaction]:
        return [
            t
            for t in self.find_all_by_user(user_id)
            if start_date <= t.date <= end_date
        ]



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

    def _to_dict(self, transaction: Transaction) -> dict:
        return {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "type": transaction.type.value,
            "amount": transaction.amount,
            "category": transaction.category,
            "date": transaction.date,
            "description": transaction.description,
        }

    def _to_model(self, data: dict) -> Transaction:
        return Transaction(
            id=data["id"],
            user_id=data["user_id"],
            type=TransactionType(data["type"]),
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data.get("description", ""),
        )

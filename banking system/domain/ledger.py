from __future__ import annotations

import uuid
from datetime import datetime
from typing import List

from domain.enums import TransactionType


class Transaction:
    def __init__(
        self,
        amount: float,
        transaction_type: TransactionType,
        description: str = "",
    ) -> None:
        self.id               = str(uuid.uuid4())
        self.amount           = amount
        self.transaction_type = transaction_type
        self.timestamp        = datetime.now()
        self.description      = description

    def __repr__(self) -> str:
        return (
            f"{self.timestamp:%Y-%m-%d %H:%M:%S}  "
            f"{self.transaction_type.value:<16}"
            f"${self.amount:>10.2f}  {self.description}"
        )


class TransactionLedger:
    def __init__(self) -> None:
        self._entries: List[Transaction] = []

    def record(
        self,
        amount: float,
        transaction_type: TransactionType,
        description: str = "",
    ) -> Transaction:
        entry = Transaction(amount, transaction_type, description)
        self._entries.append(entry)
        return entry

    def all_entries(self) -> List[Transaction]:
        return list(self._entries)

    def is_empty(self) -> bool:
        return len(self._entries) == 0

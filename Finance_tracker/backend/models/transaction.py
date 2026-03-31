from dataclasses import dataclass
from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    id: str
    user_id: str
    type: TransactionType
    amount: float
    category: str
    date: str
    description: str = ""

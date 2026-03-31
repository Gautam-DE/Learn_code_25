from dataclasses import dataclass


@dataclass
class Budget:
    id: str
    user_id: str
    category: str
    month: str          # Format: "YYYY-MM"
    limit_amount: float
    spent_amount: float = 0.0

    def is_exceeded(self) -> bool:
        return self.spent_amount > self.limit_amount

    def remaining_amount(self) -> float:
        return self.limit_amount - self.spent_amount

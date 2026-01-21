from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OrderItem:
    sku: str
    quantity: int


@dataclass
class Order:
    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    payment_method: str
    status: str = "Pending"
    transaction_id: Optional[str] = None


@dataclass
class PaymentResult:
    is_successful: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class OrderResult:
    succeeded: bool
    message: str
    transaction_id: Optional[str] = None
    details: dict = field(default_factory=dict)

    @classmethod
    def success(cls, transaction_id: str) -> "OrderResult":
        return cls(True, "Order processed", transaction_id)

    @classmethod
    def failed(cls, reason: str) -> "OrderResult":
        return cls(False, reason)

    @classmethod
    def invalid(cls, reason: str) -> "OrderResult":
        return cls(False, reason)


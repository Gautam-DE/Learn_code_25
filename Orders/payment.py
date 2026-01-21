from typing import Protocol

from .models import PaymentResult


class PaymentGateway(Protocol):
    def process_payment(self, customer_id: str, amount: float, method: str) -> PaymentResult:
        ...

    def refund_payment(self, transaction_id: str) -> None:
        ...


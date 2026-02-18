import decimal
import logging
import time
from datetime import datetime
from typing import Dict, Any

# Mocking dependent classes to make the code functional for the user
class PaymentRequest:
    def __init__(self, customer_id: str, amount: decimal.Decimal):
        self.customer_id = customer_id
        self.amount = amount

class PaymentResult:
    def __init__(self, success: bool, message: str, transaction_id: str = None):
        self.success = success
        self.message = message
        self.transaction_id = transaction_id

class NotificationService:
    def send(self, customer_id: str, message: str):
        pass

class PaymentException(Exception):
    pass

class PaymentRecord:
    def __init__(self, customer_id: str, amount: decimal.Decimal, timestamp: datetime):
        self.customer_id = customer_id
        self.amount = amount
        self.timestamp = timestamp

class PaymentProcessor:
    # Constants
    MIN_AMOUNT = decimal.Decimal("0.01")
    MAX_RETRIES = 2
    PAYMENT_SUCCESS = "Payment successful"
    PAYMENT_FAILED = "Payment failed"

    def __init__(self, logger: logging.Logger, notifier: NotificationService):
        self.logger = logger
        self.notifier = notifier
        self.history: Dict[str, PaymentRecord] = {}

    def process(self, request: PaymentRequest) -> PaymentResult:
        self._validate(request)
        
        attempt = 0
        while attempt < self.MAX_RETRIES:
            try:
                self._execute(request)
                self._record(request)
                self._notify_success(request)
                
                return PaymentResult(
                    True, 
                    self.PAYMENT_SUCCESS, 
                    self._generate_id()
                )
            except PaymentException:
                attempt += 1
                self.logger.info(f"Retry attempt: {attempt}")

        return PaymentResult(False, self.PAYMENT_FAILED, None)

    def _validate(self, request: PaymentRequest) -> None:
        if not request.customer_id or not request.customer_id.strip():
            raise ValueError("Customer ID required")

        if request.amount is None or request.amount < self.MIN_AMOUNT:
            raise ValueError("Invalid amount")

    def _execute(self, request: PaymentRequest) -> None:
        self.logger.info(f"Executing payment of {request.amount}")
        
        limit = decimal.Decimal("5000")
        if request.amount > limit:
            raise PaymentException("Limit exceeded")

    def _record(self, request: PaymentRequest) -> None:
        transaction_id = self._generate_id()
        record = PaymentRecord(
            request.customer_id, 
            request.amount, 
            datetime.now()
        )
        self.history[transaction_id] = record

    def _notify_success(self, request: PaymentRequest) -> None:
        message = f"Payment of {request.amount} processed"
        self.notifier.send(request.customer_id, message)

    def _generate_id(self) -> str:
        return f"TXN-{int(time.time() * 1000)}"

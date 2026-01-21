class OrderError(Exception):
    """Base class for order-related errors."""


class OrderNotFoundError(OrderError):
    def __init__(self, order_id: str) -> None:
        super().__init__(f"Order '{order_id}' not found")
        self.order_id = order_id


class InventoryError(OrderError):
    """Raised when inventory operations fail."""


class PaymentError(OrderError):
    """Raised when payment operations fail."""


class NotificationError(OrderError):
    """Raised when notification delivery fails."""


class OrderProcessingError(OrderError):
    """Raised when an order cannot be processed."""


class OrderCancellationError(OrderError):
    """Raised when an order cannot be cancelled."""


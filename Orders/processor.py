from .errors import (
    OrderCancellationError,
    OrderNotFoundError,
    OrderProcessingError,
)
from .inventory import InventoryService
from .models import Order, OrderResult
from .notifications import NotificationService
from .payment import PaymentGateway
from .repository import OrderRepository
from .validation import OrderValidator


class OrderProcessor:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        inventory_service: InventoryService,
        notification_service: NotificationService,
        order_repository: OrderRepository,
        order_validator: OrderValidator | None = None,
    ) -> None:
        self._payment_gateway = payment_gateway
        self._inventory_service = inventory_service
        self._notification_service = notification_service
        self._order_repository = order_repository
        self._order_validator = order_validator or OrderValidator()

    def process_order(self, order: Order) -> OrderResult:
        if order is None:
            raise ValueError("order must not be None")

        if not self._order_validator.is_valid(order):
            return OrderResult.invalid("Order validation failed")

        if not self._inventory_service.has_inventory(order.items):
            return OrderResult.failed("Insufficient inventory")

        self._inventory_service.reserve_items(order.items)

        try:
            payment = self._payment_gateway.process_payment(
                order.customer_id, order.total_amount, order.payment_method
            )
            if not payment.is_successful:
                self._inventory_service.release_reservation(order.items)
                return OrderResult.failed(f"Payment failed: {payment.error_message or 'unknown error'}")

            self._inventory_service.commit_reservation(order.items)
            self._notification_service.send_order_confirmation(order)
            order.transaction_id = payment.transaction_id
            order.status = "Paid"
            self._order_repository.save(order)
            return OrderResult.success(payment.transaction_id or "")
        except Exception as exc:
            self._inventory_service.release_reservation(order.items)
            raise OrderProcessingError("Failed to process order") from exc

    def cancel_order(self, order_id: str) -> None:
        try:
            order = self._order_repository.get_by_id(order_id)
        except OrderNotFoundError as exc:
            raise
        except Exception as exc:
            raise OrderCancellationError(f"Failed to load order '{order_id}'") from exc

        try:
            if order.status == "Paid":
                self._payment_gateway.refund_payment(order.transaction_id or "")
                self._inventory_service.restore_inventory(order.items)
            order.status = "Cancelled"
            self._order_repository.save(order)
        except Exception as exc:
            raise OrderCancellationError(f"Failed to cancel order '{order_id}'") from exc


from typing import Protocol

from .models import Order


class NotificationService(Protocol):
    def send_order_confirmation(self, order: Order) -> None:
        ...


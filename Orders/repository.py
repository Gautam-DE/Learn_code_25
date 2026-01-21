from typing import Dict, Protocol

from .errors import OrderNotFoundError
from .models import Order


class OrderRepository(Protocol):
    def get_by_id(self, order_id: str) -> Order:
        ...

    def save(self, order: Order) -> None:
        ...


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: Dict[str, Order] = {}

    def get_by_id(self, order_id: str) -> Order:
        try:
            return self._orders[order_id]
        except KeyError as exc:
            raise OrderNotFoundError(order_id) from exc

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


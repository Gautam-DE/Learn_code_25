from typing import Protocol, List

from .models import OrderItem


class InventoryService(Protocol):
    def has_inventory(self, items: List[OrderItem]) -> bool:
        ...

    def reserve_items(self, items: List[OrderItem]) -> None:
        ...

    def commit_reservation(self, items: List[OrderItem]) -> None:
        ...

    def release_reservation(self, items: List[OrderItem]) -> None:
        ...

    def restore_inventory(self, items: List[OrderItem]) -> None:
        ...


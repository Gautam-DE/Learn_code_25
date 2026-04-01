from abc import ABC, abstractmethod


class NotificationPort(ABC):
    """
    Boundary interface for sending notifications.
    Business logic depends only on this abstraction, never on a concrete implementation.
    """

    @abstractmethod
    def send_budget_exceeded_alert(
        self, category: str, spent: float, limit: float
    ) -> None:
        pass

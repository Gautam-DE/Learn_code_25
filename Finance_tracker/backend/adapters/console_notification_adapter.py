from backend.adapters.notification_port import NotificationPort


class ConsoleNotificationAdapter(NotificationPort):
    """
    Adapter that delivers budget-exceeded notifications via console output.
    Swap this class for an EmailNotificationAdapter or SMSNotificationAdapter
    without changing any business logic.
    """

    def send_budget_exceeded_alert(
        self, category: str, spent: float, limit: float
    ) -> None:
        overage = spent - limit
        print(
            f"\nAlert: '{category}' budget exceeded by "
            f"₹{overage:.2f}  (Spent: ₹{spent:.2f} / Limit: ₹{limit:.2f})"
        )

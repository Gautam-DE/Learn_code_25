from .models import Order


class OrderValidator:
    def is_valid(self, order: Order) -> bool:
        return bool(order and order.items and order.total_amount > 0)


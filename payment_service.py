class Wallet:
    def __init__(self, initial_balance: float):
        self._balance = initial_balance

    def try_deduct(self, amount: float) -> bool:
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False


class Customer:
    def __init__(self, first_name: str, last_name: str, wallet: Wallet):
        self.first_name = first_name
        self.last_name = last_name
        self._wallet = wallet

    def pay(self, amount: float) -> bool:
        return self._wallet.try_deduct(amount) if self._wallet else False


class Paperboy:
    def collect_payment(self, customer: Customer, due_amount: float):
        if not customer.pay(due_amount):
            self._schedule_return_visit()
            print(f"Customer {customer.first_name} couldn't pay ${due_amount:.2f}. Will return later.")
        else:
            print(f"Successfully collected ${due_amount:.2f} from {customer.first_name}.")

    def _schedule_return_visit(self):
        pass


if __name__ == "__main__":
    wallet = Wallet(50.0)
    customer = Customer("John", "Doe", wallet)
    paperboy = Paperboy()

    print("Paperboy tries to collect $20.00")
    paperboy.collect_payment(customer, 20.0)

    print("\nPaperboy tries to collect $40.00")
    paperboy.collect_payment(customer, 40.0)

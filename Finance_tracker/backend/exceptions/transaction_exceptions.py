class TransactionNotFoundError(Exception):
    def __init__(self, transaction_id: str):
        super().__init__(f"Transaction with id '{transaction_id}' not found.")
        self.transaction_id = transaction_id


class InvalidTransactionTypeError(Exception):
    def __init__(self, transaction_type: str):
        super().__init__(
            f"Invalid transaction type: '{transaction_type}'. Must be 'income' or 'expense'."
        )
        self.transaction_type = transaction_type


class InvalidAmountError(Exception):
    def __init__(self, amount: float):
        super().__init__(f"Amount must be a positive number, got: {amount}")
        self.amount = amount

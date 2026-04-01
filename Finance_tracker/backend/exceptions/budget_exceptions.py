class BudgetNotFoundError(Exception):
    def __init__(self, category: str, month: str):
        super().__init__(f"No budget found for category '{category}' in month '{month}'.")
        self.category = category
        self.month = month


class BudgetAlreadyExistsError(Exception):
    def __init__(self, category: str, month: str):
        super().__init__(
            f"Budget for category '{category}' in month '{month}' already exists."
        )
        self.category = category
        self.month = month

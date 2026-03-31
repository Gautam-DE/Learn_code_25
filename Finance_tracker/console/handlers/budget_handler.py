from backend.controllers.budget_controller import BudgetController
from backend.exceptions.budget_exceptions import BudgetAlreadyExistsError


class BudgetHandler:
    def __init__(self, budget_controller: BudgetController):
        self._controller = budget_controller

    def handle_set_budget(self, user_id: str) -> None:
        print("\nSet Monthly Budget")
        category = input("Category: ").strip()
        month = input("Month (YYYY-MM): ").strip()
        limit = self._prompt_for_valid_limit()

        try:
            budget = self._controller.set_budget(user_id, category, month, limit)
            print(
                f"\nSuccess: Budget set at ₹{budget['limit_amount']:.2f} for "
                f"'{budget['category']}' in {budget['month']}."
            )
        except BudgetAlreadyExistsError as error:
            print(f"\nError: {error}")

    def handle_get_budgets(self, user_id: str) -> None:
        print("\nYour Budgets")
        budgets = self._controller.get_budgets(user_id)

        if not budgets:
            print("No budgets set.")
            return

        self._display_budgets(budgets)



    def _display_budgets(self, budgets: list) -> None:
        header = (
            f"{'Category':<14}  {'Month':<8}  {'Limit':>10}  "
            f"{'Spent':>10}  {'Remaining':>10}  Status"
        )
        print("\n" + header)
        for b in budgets:
            status = "EXCEEDED" if b["is_exceeded"] else "OK"
            print(
                f"{b['category']:<14}  {b['month']:<8}  "
                f"₹{b['limit_amount']:>9.2f}  ₹{b['spent_amount']:>9.2f}  "
                f"₹{b['remaining']:>9.2f}  {status}"
            )

    def _prompt_for_valid_limit(self) -> float:
        while True:
            try:
                return float(input("Monthly limit (₹): ").strip())
            except ValueError:
                print("Error: Please enter a valid number.")

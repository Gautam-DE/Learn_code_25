from typing import Optional

from backend.controllers.transaction_controller import TransactionController
from backend.exceptions.transaction_exceptions import (
    TransactionNotFoundError,
    InvalidTransactionTypeError,
    InvalidAmountError,
)


class TransactionHandler:
    def __init__(self, transaction_controller: TransactionController):
        self._controller = transaction_controller

    def handle_add_transaction(self, user_id: str) -> None:
        print("\nAdd Transaction")
        transaction_type = input("Type (income / expense): ").strip()
        amount = self._prompt_for_valid_amount()
        category = input("Category (e.g. food, rent, salary): ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        description = input("Description (optional): ").strip()

        try:
            transaction = self._controller.add_transaction(
                user_id, transaction_type, amount, category, date, description
            )
            print(f"\nSuccess: Transaction added. ID: {transaction['id']}")
        except (InvalidTransactionTypeError, InvalidAmountError) as error:
            print(f"\nError: {error}")

    def handle_get_transactions(self, user_id: str) -> None:
        print("\nView Transactions")
        print("Filter: 1. By Category   2. By Date Range   3. All")
        choice = input("Choice: ").strip()

        try:
            transactions = self._fetch_with_filter(user_id, choice)
            if not transactions:
                print("\nNo transactions found.")
                return
            self._display_transactions(transactions)
        except Exception as error:
            print(f"\nError: {error}")

    def handle_delete_transaction(self) -> None:
        print("\nDelete Transaction")
        transaction_id = input("Transaction ID: ").strip()
        try:
            result = self._controller.delete_transaction(transaction_id)
            print(f"\nSuccess: {result['message']}")
        except TransactionNotFoundError as error:
            print(f"\nError: {error}")



    def _fetch_with_filter(self, user_id: str, choice: str) -> list:
        if choice == "1":
            category = input("Category: ").strip()
            return self._controller.get_transactions(user_id, category=category)
        if choice == "2":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date   (YYYY-MM-DD): ").strip()
            return self._controller.get_transactions(
                user_id, start_date=start_date, end_date=end_date
            )
        return self._controller.get_transactions(user_id)

    def _display_transactions(self, transactions: list) -> None:
        header = (
            f"{'ID':<36}  {'Type':<8}  {'Amount':>10}  "
            f"{'Category':<14}  {'Date':<12}  Description"
        )
        print("\n" + header)
        for t in transactions:
            print(
                f"{t['id']:<36}  {t['type']:<8}  ₹{t['amount']:>9.2f}  "
                f"{t['category']:<14}  {t['date']:<12}  {t['description']}"
            )

    def _prompt_for_valid_amount(self) -> float:
        while True:
            try:
                return float(input("Amount: ").strip())
            except ValueError:
                print("Error: Please enter a valid number.")

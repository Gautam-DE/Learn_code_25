from __future__ import annotations
from typing import Optional


class BankingError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason: str = reason

    def __str__(self) -> str:
        return self.reason


class InsufficientFundsError(BankingError):
    def __init__(
        self,
        available: float,
        requested: float,
        account_ref: Optional[str] = None,
    ) -> None:
        self.available   = available
        self.requested   = requested
        self.account_ref = account_ref

        location = f" on account [{account_ref}]" if account_ref else ""
        super().__init__(
            f"Insufficient funds{location}: "
            f"available ${available:.2f}, requested ${requested:.2f}."
        )


class AmountValidationError(BankingError):
    def __init__(
        self,
        field_name: str,
        received_value: float,
        constraint: str = "must be greater than zero",
    ) -> None:
        self.field_name     = field_name
        self.received_value = received_value
        self.constraint     = constraint

        super().__init__(
            f"'{field_name}' {constraint} (received {received_value})."
        )


class EmptyFieldError(BankingError):
    def __init__(self, field_name: str) -> None:
        self.field_name = field_name
        super().__init__(f"'{field_name}' cannot be empty or blank.")


class InvalidLoanError(BankingError):
    def __init__(
        self,
        loan_id: str,
        current_status: str,
        attempted_action: str = "perform an operation",
    ) -> None:
        self.loan_id          = loan_id
        self.current_status   = current_status
        self.attempted_action = attempted_action

        super().__init__(
            f"Cannot {attempted_action} on loan [{loan_id}]: "
            f"loan is currently '{current_status}'."
        )


class AccountNotFoundError(BankingError):
    def __init__(self, account_number: str) -> None:
        self.account_number = account_number
        super().__init__(f"Account [{account_number}] could not be found.")

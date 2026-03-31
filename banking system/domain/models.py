from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import List

from domain.enums import TransactionType, LoanStatus
from domain.exceptions import AmountValidationError, InsufficientFundsError
from domain.ledger import TransactionLedger, Transaction
from utils.validation import (
    validate_positive_amount,
    validate_non_negative_amount,
    validate_non_empty_string,
    validate_sufficient_funds,
)


class Customer:
    def __init__(self, name: str, email: str) -> None:
        validate_non_empty_string(name, "Customer Name")
        validate_non_empty_string(email, "Customer Email")
        self.id    = str(uuid.uuid4())
        self.name  = name
        self.email = email

    def __repr__(self) -> str:
        return f"Customer(id={self.id[:8]}, name={self.name})"


class Account(ABC):
    def __init__(self, customer: Customer, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise AmountValidationError(
                field_name="Initial Balance",
                received_value=initial_balance,
                constraint="cannot be negative",
            )
        self._account_number = str(uuid.uuid4())
        self._customer        = customer
        self._balance         = initial_balance
        self._ledger          = TransactionLedger()

        if initial_balance > 0:
            self._ledger.record(initial_balance, TransactionType.DEPOSIT, "Initial deposit")

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def transactions(self) -> List[Transaction]:
        return self._ledger.all_entries()

    def deposit(self, amount: float, description: str = "") -> Transaction:
        validate_positive_amount(amount, "Deposit Amount")
        self._balance += amount
        return self._ledger.record(amount, TransactionType.DEPOSIT, description)

    def withdraw(self, amount: float, description: str = "") -> Transaction:
        validate_positive_amount(amount, "Withdrawal Amount")
        self._ensure_sufficient_funds(amount)
        self._balance -= amount
        return self._ledger.record(amount, TransactionType.WITHDRAWAL, description)

    def debit_transfer(self, amount: float, to_account_number: str) -> Transaction:
        validate_positive_amount(amount, "Transfer Amount")
        self._ensure_sufficient_funds(amount)
        self._balance -= amount
        return self._ledger.record(
            amount,
            TransactionType.TRANSFER_OUT,
            f"Transfer to account {to_account_number[:8]}",
        )

    def credit_transfer(self, amount: float, from_account_number: str) -> Transaction:
        validate_positive_amount(amount, "Transfer Amount")
        self._balance += amount
        return self._ledger.record(
            amount,
            TransactionType.TRANSFER_IN,
            f"Transfer from account {from_account_number[:8]}",
        )

    @abstractmethod
    def get_account_type(self) -> str:
        ...

    def _ensure_sufficient_funds(self, amount: float) -> None:
        validate_sufficient_funds(self._balance, amount)

    def __repr__(self) -> str:
        return (
            f"{self.get_account_type()}Account("
            f"number={self._account_number[:8]}, "
            f"balance=${self._balance:.2f})"
        )


class SavingsAccount(Account):
    DEFAULT_INTEREST_RATE = 0.03

    def __init__(
        self,
        customer: Customer,
        initial_balance: float = 0.0,
        interest_rate: float = DEFAULT_INTEREST_RATE,
    ) -> None:
        super().__init__(customer, initial_balance)
        validate_non_negative_amount(interest_rate, "Interest Rate")
        self._interest_rate = interest_rate

    @property
    def interest_rate(self) -> float:
        return self._interest_rate

    def get_account_type(self) -> str:
        return "Savings"

    def apply_monthly_interest(self) -> Transaction:
        interest_amount = self._balance * self._interest_rate
        self._balance  += interest_amount
        return self._ledger.record(
            interest_amount,
            TransactionType.INTEREST,
            f"Monthly interest at {self._interest_rate * 100:.1f}%",
        )


class CurrentAccount(Account):
    DEFAULT_OVERDRAFT_LIMIT = 500.0

    def __init__(
        self,
        customer: Customer,
        initial_balance: float = 0.0,
        overdraft_limit: float = DEFAULT_OVERDRAFT_LIMIT,
    ) -> None:
        super().__init__(customer, initial_balance)
        self._overdraft_limit = overdraft_limit

    @property
    def overdraft_limit(self) -> float:
        return self._overdraft_limit

    def get_account_type(self) -> str:
        return "Current"

    def _ensure_sufficient_funds(self, amount: float) -> None:
        effective_limit = self._balance + self._overdraft_limit
        if effective_limit < amount:
            raise InsufficientFundsError(
                available=effective_limit,
                requested=amount,
                account_ref=self._account_number[:8],
            )


class Loan:
    def __init__(
        self,
        customer: Customer,
        principal_amount: float,
        annual_interest_rate: float,
    ) -> None:
        validate_positive_amount(principal_amount, "Principal Amount")
        validate_non_negative_amount(annual_interest_rate, "Annual Interest Rate")

        self.id                    = str(uuid.uuid4())
        self._customer             = customer
        self._principal_amount     = principal_amount
        self._annual_interest_rate = annual_interest_rate
        self._outstanding_balance  = principal_amount
        self._status               = LoanStatus.ACTIVE

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def principal_amount(self) -> float:
        return self._principal_amount

    @property
    def annual_interest_rate(self) -> float:
        return self._annual_interest_rate

    @property
    def interest_rate(self) -> float:
        return self._annual_interest_rate

    @property
    def outstanding_balance(self) -> float:
        return self._outstanding_balance

    @property
    def status(self) -> LoanStatus:
        return self._status

    @property
    def is_active(self) -> bool:
        return self._status == LoanStatus.ACTIVE

    def make_repayment(self, amount: float) -> None:
        validate_positive_amount(amount, "Repayment Amount")
        applied = min(amount, self._outstanding_balance)
        self._outstanding_balance -= applied
        if self._outstanding_balance <= 1e-9:
            self._outstanding_balance = 0.0
            self._status = LoanStatus.REPAID

    def __repr__(self) -> str:
        return (
            f"Loan(id={self.id[:8]}, "
            f"principal=${self._principal_amount:.2f}, "
            f"outstanding=${self._outstanding_balance:.2f}, "
            f"status={self._status.value})"
        )

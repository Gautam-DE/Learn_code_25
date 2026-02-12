"""Domain models for the Banking System."""
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from utils.validators import validate_positive_amount, validate_non_empty_string, validate_sufficient_funds

class Customer:
    def __init__(self, name: str, email: str):
        self._validate_customer_details(name, email)
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email

    def _validate_customer_details(self, name: str, email: str):
        validate_non_empty_string(name, "Customer Name")
        validate_non_empty_string(email, "Customer Email")

    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name})"


class Transaction:
    def __init__(self, amount: float, transaction_type: str, description: str = ""):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.now()
        self.description = description

    def __repr__(self):
        return f"[{self.timestamp}] {self.transaction_type}: {self.amount} ({self.description})"


class Account(ABC):
    def __init__(self, customer: Customer, balance: float = 0.0):
        self.account_number = str(uuid.uuid4())
        self.customer = customer
        self.balance = balance
        self.transactions: List[Transaction] = []

    def deposit(self, amount: float) -> None:
        validate_positive_amount(amount, "Deposit Amount")
        self.balance += amount
        self._record_transaction(amount, "DEPOSIT")

    def withdraw(self, amount: float) -> None:
        validate_positive_amount(amount, "Withdrawal Amount")
        validate_sufficient_funds(self.balance, amount)
        self.balance -= amount
        self._record_transaction(amount, "WITHDRAWAL")

    @abstractmethod
    def get_account_type(self) -> str:
        pass

    def _record_transaction(self, amount: float, txn_type: str) -> None:
        self.transactions.append(Transaction(amount, txn_type))


class SavingsAccount(Account):
    def get_account_type(self) -> str:
        return "Savings"


class CheckingAccount(Account):
    def get_account_type(self) -> str:
        return "Checking"


class Loan:
    def __init__(self, customer: Customer, principal_amount: float, interest_rate: float):
        validate_positive_amount(principal_amount, "Principal Amount")
        self.id = str(uuid.uuid4())
        self.customer = customer
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.is_active = True

    def __repr__(self):
        return f"Loan({self.id}, Principal={self.principal_amount}, Rate={self.interest_rate}%)"

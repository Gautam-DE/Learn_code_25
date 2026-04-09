from __future__ import annotations
from typing import List

from domain.exceptions import InvalidLoanError
from domain.interfaces import InterestStrategy
from domain.models import Customer, Loan
from utils.validation import validate_positive_amount


class LoanService:
    def __init__(self, interest_strategy: InterestStrategy) -> None:
        self._strategy     = interest_strategy
        self._issued_loans: List[Loan] = []

    def create_loan(self, customer: Customer, principal: float, annual_rate: float) -> Loan:
        loan = Loan(customer, principal, annual_rate)
        self._issued_loans.append(loan)
        return loan

    def calculate_interest_due(self, loan: Loan, years: float) -> float:
        return self._strategy.calculate(loan.principal_amount, loan.annual_interest_rate, years)

    def repay_loan(self, loan: Loan, amount: float) -> None:
        if not loan.is_active:
            raise InvalidLoanError(
                loan_id=loan.id[:8],
                current_status=loan.status.value,
                attempted_action="apply a repayment",
            )
        loan.make_repayment(amount)

    def get_active_loans_for(self, customer: Customer) -> List[Loan]:
        return [
            loan for loan in self._issued_loans
            if loan.customer is customer and loan.is_active
        ]

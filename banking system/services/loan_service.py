from domain.models import Loan, Customer
from domain.interfaces import InterestStrategy

class LoanService:
    """
    Manages loan issuance and calculations.
    """
    def __init__(self, strategy: InterestStrategy):
        self.strategy = strategy
        self.loans = []

    def grant_loan(self, customer: Customer, principal: float, rate: float) -> Loan:
        loan = Loan(customer, principal, rate)
        self.loans.append(loan)
        return loan

    def get_interest_due(self, loan: Loan, years: float) -> float:
        return self.strategy.calculate(loan.principal_amount, loan.interest_rate, years)

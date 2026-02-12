"""Interest Calculation Strategies."""
from domain.interfaces import InterestStrategy

class SimpleInterest(InterestStrategy):

    
    def calculate(self, principal: float, rate: float, time: float) -> float:
        return (principal * rate * time) / 100


class CompoundInterest(InterestStrategy):

    
    def calculate(self, principal: float, rate: float, time: float) -> float:
        amount_accumulated = principal * ((1 + (rate / 100)) ** time)
        interest_only = amount_accumulated - principal
        return interest_only

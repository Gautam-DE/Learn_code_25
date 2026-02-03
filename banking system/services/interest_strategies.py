from domain.interfaces import InterestStrategy

class SimpleInterest(InterestStrategy):
    """Simple Interest formula: (P * R * T) / 100"""
    
    def calculate(self, principal: float, rate: float, time: float) -> float:
        return (principal * rate * time) / 100

class CompoundInterest(InterestStrategy):
    """Compound Interest formula"""

    def calculate(self, principal: float, rate: float, time: float) -> float:
        # A = P(1 + r/100)^t
        amount = principal * ((1 + (rate / 100)) ** time)
        return amount - principal

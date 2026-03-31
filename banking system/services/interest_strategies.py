from domain.interfaces import InterestStrategy


class SimpleInterest(InterestStrategy):
    def calculate(self, principal: float, rate: float, time_in_years: float) -> float:
        return (principal * rate * time_in_years) / 100


class CompoundInterest(InterestStrategy):
    def calculate(self, principal: float, rate: float, time_in_years: float) -> float:
        accumulated_amount = principal * ((1 + rate / 100) ** time_in_years)
        return accumulated_amount - principal

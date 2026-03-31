from abc import ABC, abstractmethod


class InterestStrategy(ABC):
    """Implementations must be stateless.
    rate is a percentage (e.g. 5.5 for 5.5%). time_in_years is in years.
    """

    @abstractmethod
    def calculate(self, principal: float, rate: float, time_in_years: float) -> float:
        ...

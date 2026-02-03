from abc import ABC, abstractmethod

class InterestStrategy(ABC):
    """
    Abstract contract for different interest calculation algorithms.
    """
    
    @abstractmethod
    def calculate(self, principal: float, rate: float, time: float) -> float:
        """
        Calculates interest. 
        Time is expected in years. Rate is a percentage (e.g. 5.5).
        """
        pass

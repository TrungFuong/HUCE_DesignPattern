from abc import ABC, abstractmethod


class RiskStrategy(ABC):

    @abstractmethod
    def evaluate(self, sensor_log, rule) -> bool:
        pass

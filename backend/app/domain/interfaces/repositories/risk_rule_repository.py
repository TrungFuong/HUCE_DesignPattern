from abc import ABC, abstractmethod

from app.domain.entities.risk_rule import RiskRule


class RiskRuleRepository(ABC):

    @abstractmethod
    async def find_by_crop_type(self, crop_type: str) -> list[RiskRule]:
        pass

    @abstractmethod
    async def save(self, risk_rule: RiskRule) -> RiskRule:
        pass

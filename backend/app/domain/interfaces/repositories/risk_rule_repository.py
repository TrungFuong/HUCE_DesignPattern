from abc import ABC, abstractmethod

from app.domain.entities.risk_rule import RiskRule


class RiskRuleRepository(ABC):

    @abstractmethod
    async def find_all(self) -> list[RiskRule]:
        pass

    @abstractmethod
    async def find_by_id(self, risk_rule_id: str) -> RiskRule | None:
        pass

    @abstractmethod
    async def find_by_crop_type_id(self, crop_type_id: str) -> list[RiskRule]:
        pass

    @abstractmethod
    async def save(self, risk_rule: RiskRule) -> RiskRule:
        pass

    @abstractmethod
    async def update(self, risk_rule: RiskRule) -> RiskRule:
        pass

    @abstractmethod
    async def delete(self, risk_rule_id: str) -> None:
        pass

from app.domain.interfaces.repositories.risk_rule_repository import RiskRuleRepository
from app.domain.interfaces.services.hash_service import HashService
from app.domain.rules.temperature_risk_strategy import TemperatureRiskStrategy
from app.domain.rules.humidity_risk_strategy import HumidityRiskStrategy
from app.domain.rules.soil_risk_strategy import SoilRiskStrategy
from app.domain.enums.risk_level import RiskLevel


class RiskService:

    def __init__(self, risk_rule_repository: RiskRuleRepository):
        self.risk_rule_repository = risk_rule_repository
        self.strategies = [
            TemperatureRiskStrategy(),
            HumidityRiskStrategy(),
            SoilRiskStrategy(),
        ]

    async def classify_sensor_log(self, sensor_log, crop_type_id: str | None = None):
        rule_key = crop_type_id or getattr(sensor_log, "crop_type_id", None) or sensor_log.batch_id
        rules = await self.risk_rule_repository.find_by_crop_type_id(rule_key)
        if not rules:
            return RiskLevel.NORMAL
        rule = rules[0]
        for strategy in self.strategies:
            if strategy.evaluate(sensor_log, rule):
                return RiskLevel.AT_RISK
        return RiskLevel.NORMAL

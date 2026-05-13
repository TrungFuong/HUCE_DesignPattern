from sqlalchemy import select

from app.domain.entities.risk_rule import RiskRule
from app.domain.interfaces.repositories.risk_rule_repository import RiskRuleRepository
from app.infrastructure.database.sqlserver.models.risk_rule_model import RiskRuleModel


class SqlRiskRuleRepository(RiskRuleRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def find_by_crop_type(self, crop_type: str) -> list[RiskRule]:
        result = await self.db_session.execute(select(RiskRuleModel).where(RiskRuleModel.crop_type == crop_type))
        return [
            RiskRule(
                id=model.id,
                crop_type=model.crop_type,
                min_temperature=model.min_temperature,
                max_temperature=model.max_temperature,
                min_humidity=model.min_humidity,
                max_humidity=model.max_humidity,
                min_soil_moisture=model.min_soil_moisture,
                max_soil_moisture=model.max_soil_moisture,
                duration_minutes=model.duration_minutes,
            )
            for model in result.scalars().all()
        ]

    async def save(self, risk_rule: RiskRule) -> RiskRule:
        model = RiskRuleModel(
            id=risk_rule.id,
            crop_type=risk_rule.crop_type,
            min_temperature=risk_rule.min_temperature,
            max_temperature=risk_rule.max_temperature,
            min_humidity=risk_rule.min_humidity,
            max_humidity=risk_rule.max_humidity,
            min_soil_moisture=risk_rule.min_soil_moisture,
            max_soil_moisture=risk_rule.max_soil_moisture,
            duration_minutes=risk_rule.duration_minutes,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return risk_rule

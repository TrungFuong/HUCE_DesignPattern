from sqlalchemy import select

from app.domain.entities.risk_rule import RiskRule
from app.domain.interfaces.repositories.risk_rule_repository import RiskRuleRepository
from app.infrastructure.database.sqlserver.models.risk_rule_model import RiskRuleModel


class SqlRiskRuleRepository(RiskRuleRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def find_all(self) -> list[RiskRule]:
        result = await self.db_session.execute(select(RiskRuleModel))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def find_by_id(self, risk_rule_id: str) -> RiskRule | None:
        model = await self.db_session.get(RiskRuleModel, risk_rule_id)
        return self._to_entity(model) if model else None

    async def find_by_crop_type_id(self, crop_type_id: str) -> list[RiskRule]:
        result = await self.db_session.execute(select(RiskRuleModel).where(RiskRuleModel.crop_type_id == crop_type_id))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def save(self, risk_rule: RiskRule) -> RiskRule:
        model = RiskRuleModel(
            id=risk_rule.id,
            crop_type_id=risk_rule.crop_type_id,
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

    async def update(self, risk_rule: RiskRule) -> RiskRule:
        model = await self.db_session.get(RiskRuleModel, risk_rule.id)
        if model is None:
            raise ValueError("Risk rule not found")
        model.crop_type_id = risk_rule.crop_type_id
        model.min_temperature = risk_rule.min_temperature
        model.max_temperature = risk_rule.max_temperature
        model.min_humidity = risk_rule.min_humidity
        model.max_humidity = risk_rule.max_humidity
        model.min_soil_moisture = risk_rule.min_soil_moisture
        model.max_soil_moisture = risk_rule.max_soil_moisture
        model.duration_minutes = risk_rule.duration_minutes
        await self.db_session.commit()
        return risk_rule

    async def delete(self, risk_rule_id: str) -> None:
        model = await self.db_session.get(RiskRuleModel, risk_rule_id)
        if model is None:
            raise ValueError("Risk rule not found")
        await self.db_session.delete(model)
        await self.db_session.commit()

    def _to_entity(self, model: RiskRuleModel) -> RiskRule:
        return RiskRule(
            id=model.id,
            crop_type_id=model.crop_type_id,
            min_temperature=model.min_temperature,
            max_temperature=model.max_temperature,
            min_humidity=model.min_humidity,
            max_humidity=model.max_humidity,
            min_soil_moisture=model.min_soil_moisture,
            max_soil_moisture=model.max_soil_moisture,
            duration_minutes=model.duration_minutes,
        )

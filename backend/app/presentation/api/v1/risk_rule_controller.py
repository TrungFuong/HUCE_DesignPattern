import uuid

from fastapi import APIRouter

from app.application.dto.risk_rule_dto import RiskRuleRequest
from app.domain.entities.risk_rule import RiskRule
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/risk-rules", tags=["Risk Rules"])


@router.post("/")
async def create_risk_rule(request: RiskRuleRequest):
    async with get_async_session() as session:
        repository = SqlRiskRuleRepository(session)
        risk_rule = RiskRule(
            id=request.id or str(uuid.uuid4()),
            crop_type=request.crop_type,
            min_temperature=request.min_temperature,
            max_temperature=request.max_temperature,
            min_humidity=request.min_humidity,
            max_humidity=request.max_humidity,
            min_soil_moisture=request.min_soil_moisture,
            max_soil_moisture=request.max_soil_moisture,
            duration_minutes=request.duration_minutes,
        )
        return await repository.save(risk_rule)


@router.get("/{crop_type}")
async def get_risk_rules(crop_type: str):
    async with get_async_session() as session:
        repository = SqlRiskRuleRepository(session)
        return await repository.find_by_crop_type(crop_type)

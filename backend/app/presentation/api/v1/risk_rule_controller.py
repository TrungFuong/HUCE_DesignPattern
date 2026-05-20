import uuid

from fastapi import APIRouter

from app.application.dto.risk_rule_dto import RiskRuleRequest
from app.domain.entities.risk_rule import RiskRule
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/risk-rules", tags=["Risk Rules"])


def validate_risk_rule(request: RiskRuleRequest) -> None:
    if not request.crop_type_id.strip():
        raise ValueError("Crop type id is required")
    if request.min_temperature > request.max_temperature:
        raise ValueError("min_temperature must be less than or equal to max_temperature")
    if request.min_humidity > request.max_humidity:
        raise ValueError("min_humidity must be less than or equal to max_humidity")
    if request.min_soil_moisture is not None and request.max_soil_moisture is not None:
        if request.min_soil_moisture > request.max_soil_moisture:
            raise ValueError("min_soil_moisture must be less than or equal to max_soil_moisture")
    if request.duration_minutes <= 0:
        raise ValueError("duration_minutes must be greater than 0")


@router.post("/")
async def create_risk_rule(request: RiskRuleRequest):
    validate_risk_rule(request)
    async with get_async_session() as session:
        crop_type = await SqlCropTypeRepository(session).find_by_id(request.crop_type_id.strip())
        if crop_type is None:
            raise ValueError("Risk rule crop_type_id does not exist")
        repository = SqlRiskRuleRepository(session)
        risk_rule = RiskRule(
            id=request.id or str(uuid.uuid4()),
            crop_type_id=request.crop_type_id.strip(),
            min_temperature=request.min_temperature,
            max_temperature=request.max_temperature,
            min_humidity=request.min_humidity,
            max_humidity=request.max_humidity,
            min_soil_moisture=request.min_soil_moisture,
            max_soil_moisture=request.max_soil_moisture,
            duration_minutes=request.duration_minutes,
        )
        return await repository.save(risk_rule)


@router.get("/{crop_type_id}")
async def get_risk_rules(crop_type_id: str):
    async with get_async_session() as session:
        repository = SqlRiskRuleRepository(session)
        return await repository.find_by_crop_type_id(crop_type_id)

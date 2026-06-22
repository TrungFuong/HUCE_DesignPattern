import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.risk_rule_dto import RiskRuleRequest
from app.domain.entities.risk_rule import RiskRule
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName

router = APIRouter(
    prefix="/risk-rules",
    tags=["Risk Rules"],
    dependencies=[Depends(require_roles(RoleName.ADMIN, RoleName.FARMER))],
)


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


async def validate_crop_type_exists(session, crop_type_id: str) -> str:
    normalized_crop_type_id = crop_type_id.strip()
    crop_type = await SqlCropTypeRepository(session).find_by_id(normalized_crop_type_id)
    if crop_type is None:
        raise ValueError("Risk rule crop_type_id does not exist")
    return normalized_crop_type_id


def build_risk_rule(request: RiskRuleRequest, risk_rule_id: str, crop_type_id: str) -> RiskRule:
    return RiskRule(
        id=risk_rule_id,
        crop_type_id=crop_type_id,
        min_temperature=request.min_temperature,
        max_temperature=request.max_temperature,
        min_humidity=request.min_humidity,
        max_humidity=request.max_humidity,
        min_soil_moisture=request.min_soil_moisture,
        max_soil_moisture=request.max_soil_moisture,
        duration_minutes=request.duration_minutes,
    )


@router.post("/")
async def create_risk_rule(request: RiskRuleRequest):
    try:
        validate_risk_rule(request)
        async with get_async_session() as session:
            crop_type_id = await validate_crop_type_exists(session, request.crop_type_id)
            repository = SqlRiskRuleRepository(session)
            risk_rule = build_risk_rule(request, request.id or str(uuid.uuid4()), crop_type_id)
            return await repository.save(risk_rule)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/")
async def list_risk_rules():
    async with get_async_session() as session:
        repository = SqlRiskRuleRepository(session)
        return await repository.find_all()


@router.get("/id/{risk_rule_id}")
async def get_risk_rule_by_id(risk_rule_id: str):
    async with get_async_session() as session:
        repository = SqlRiskRuleRepository(session)
        risk_rule = await repository.find_by_id(risk_rule_id)
        if risk_rule is None:
            raise HTTPException(status_code=404, detail="Risk rule not found")
        return risk_rule


@router.put("/id/{risk_rule_id}")
async def update_risk_rule(risk_rule_id: str, request: RiskRuleRequest):
    try:
        validate_risk_rule(request)
        async with get_async_session() as session:
            repository = SqlRiskRuleRepository(session)
            existing = await repository.find_by_id(risk_rule_id)
            if existing is None:
                raise HTTPException(status_code=404, detail="Risk rule not found")
            crop_type_id = await validate_crop_type_exists(session, request.crop_type_id)
            risk_rule = build_risk_rule(request, risk_rule_id, crop_type_id)
            return await repository.update(risk_rule)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/id/{risk_rule_id}")
async def delete_risk_rule(risk_rule_id: str):
    try:
        async with get_async_session() as session:
            repository = SqlRiskRuleRepository(session)
            await repository.delete(risk_rule_id)
            return {"message": "Risk rule deleted successfully"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{crop_type_id}")
async def get_risk_rules(crop_type_id: str):
    async with get_async_session() as session:
        repository = SqlRiskRuleRepository(session)
        return await repository.find_by_crop_type_id(crop_type_id)

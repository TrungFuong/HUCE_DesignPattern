from fastapi import APIRouter, Depends

from app.application.dto.chemical_dto import ChemicalRequest
from app.application.services.chemical_service import ChemicalService
from app.core.dependencies import get_current_user, require_roles
from app.domain.enums.role import RoleName
from app.infrastructure.database.sqlserver.repositories.sql_chemical_repository import SqlChemicalRepository
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/chemicals", tags=["Chemicals"])


def create_chemical_service(session) -> ChemicalService:
    return ChemicalService(
        chemical_repository=SqlChemicalRepository(session),
        crop_type_repository=SqlCropTypeRepository(session),
    )


# ──────────── Admin-only: CRUD hóa chất ────────────

@router.post("/")
async def create_chemical(
    request: ChemicalRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    """Tạo hóa chất mới — chỉ Admin."""
    async with get_async_session() as session:
        return await create_chemical_service(session).create_chemical(request)


@router.put("/{chemical_id}")
async def update_chemical(
    chemical_id: str,
    request: ChemicalRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    """Cập nhật hóa chất — chỉ Admin."""
    async with get_async_session() as session:
        return await create_chemical_service(session).update_chemical(chemical_id, request)


@router.delete("/{chemical_id}")
async def delete_chemical(
    chemical_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    """Xóa mềm hóa chất — chỉ Admin."""
    async with get_async_session() as session:
        return await create_chemical_service(session).delete_chemical(chemical_id)


# ──────────── Admin + Farmer: đọc danh sách hóa chất ────────────

@router.get("/")
async def list_all_chemicals(
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    """Danh sách tất cả hóa chất — Admin + Farmer (farmer cần xem để chọn)."""
    async with get_async_session() as session:
        return await create_chemical_service(session).list_all()


@router.get("/crop-type/{crop_type_id}")
async def list_chemicals_by_crop_type(
    crop_type_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    """Danh sách hóa chất theo loại nông sản — Admin + Farmer."""
    async with get_async_session() as session:
        return await create_chemical_service(session).list_by_crop_type(crop_type_id)

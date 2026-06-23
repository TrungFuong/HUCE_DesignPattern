from fastapi import APIRouter, Depends, Query

from app.application.dto.user_dto import CreateUserRequest, UpdateUserRequest
from app.application.services.user_service import UserService
from app.core.dependencies import get_current_user, require_roles
from app.domain.enums.role import RoleName
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def list_users(
    role: int | None = Query(default=None),
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        users = await UserService(SqlUserRepository(session)).list_users(role)
        return [to_user_response(user) for user in users]


@router.post("/")
async def create_user(
    request: CreateUserRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        user = await UserService(SqlUserRepository(session)).create_user(request)
        return to_user_response(user)


@router.get("/lookup")
async def list_user_lookup(
    current_user: dict = Depends(
        require_roles(RoleName.ADMIN, RoleName.TRADER, RoleName.DISTRIBUTOR)
    ),
):
    async with get_async_session() as session:
        users = await UserService(SqlUserRepository(session)).list_users()
        return [to_user_response(user) for user in users if user.is_active]


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        user = await UserService(SqlUserRepository(session)).get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        return to_user_response(user)


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        user = await UserService(SqlUserRepository(session)).update_user(user_id, request)
        return to_user_response(user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        success = await UserService(SqlUserRepository(session)).delete_user(user_id)
        return {"success": success}


def to_user_response(user):
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": int(user.role),
        "is_active": user.is_active,
        "created_at": user.created_at,
    }

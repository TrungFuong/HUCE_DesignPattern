from fastapi import APIRouter, Depends, Query

from app.application.services.user_service import UserService
from app.core.dependencies import get_current_user
from app.application.dto.user_dto import UpdateUserRequest
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def list_users(
    role: int | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        user_service = UserService(SqlUserRepository(session))
        users = await user_service.list_users(role)
        return [to_user_response(user) for user in users]


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Lấy thông tin user hiện đang đăng nhập từ JWT token."""
    return current_user


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        user_service = UserService(SqlUserRepository(session))
        user = await user_service.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        return to_user_response(user)


@router.put("/{user_id}")
async def update_user(user_id: str, request: UpdateUserRequest):
    async with get_async_session() as session:
        user_service = UserService(SqlUserRepository(session))
        user = await user_service.update_user(user_id, request)
        return to_user_response(user)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    async with get_async_session() as session:
        user_service = UserService(SqlUserRepository(session))
        success = await user_service.delete_user(user_id)
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

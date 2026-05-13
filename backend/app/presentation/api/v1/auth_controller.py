from fastapi import APIRouter, Depends
from app.application.dto.auth_dto import LoginRequest, RegisterRequest
from app.application.services.auth_service import AuthService
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(request: RegisterRequest):
    async with get_async_session() as session:
        auth_service = AuthService(SqlUserRepository(session))
        return await auth_service.register(request)


@router.post("/login")
async def login(request: LoginRequest):
    async with get_async_session() as session:
        auth_service = AuthService(SqlUserRepository(session))
        return await auth_service.login(request)

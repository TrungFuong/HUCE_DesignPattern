from fastapi import APIRouter, Depends
from app.application.dto.auth_dto import LoginRequest, RegisterRequest, ChangePasswordRequest
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


from app.core.dependencies import get_current_user
from app.presentation.api.v1.user_controller import to_user_response
from fastapi import HTTPException

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    async with get_async_session() as session:
        user_repo = SqlUserRepository(session)
        user = await user_repo.find_by_email(current_user["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return to_user_response(user)

@router.put("/change-password")
async def change_password(request: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    async with get_async_session() as session:
        auth_service = AuthService(SqlUserRepository(session))
        await auth_service.change_password(
            email=current_user["sub"],
            old_password=request.old_password,
            new_password=request.new_password
        )
        return {"message": "Password changed successfully"}

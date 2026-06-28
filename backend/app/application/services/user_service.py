from app.domain.interfaces.repositories.user_repository import UserRepository
from app.domain.enums.role import RoleName
from app.application.dto.user_dto import UpdateUserRequest

class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: str):
        return await self.user_repository.find_by_id(user_id)

    async def list_users(self, role: int | None = None):
        users = await self.user_repository.find_all()
        if role is None:
            return users
        role_name = RoleName(role)
        return [user for user in users if user.role == role_name]

    async def update_user(self, user_id: str, request: UpdateUserRequest):
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if user.email == "admin@ocop.vn":
            raise ValueError("Không thể sửa tài khoản Admin mặc định")
        
        if request.email and request.email != user.email:
            existing_user = await self.user_repository.find_by_email(request.email)
            if existing_user:
                raise ValueError("Email already in use")

        role_enum = RoleName(request.role) if request.role is not None else None
        user.update_info(
            full_name=request.full_name,
            email=request.email,
            role=role_enum,
            is_active=request.is_active
        )
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: str):
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if user.email == "admin@ocop.vn":
            raise ValueError("Không thể xóa tài khoản Admin mặc định")
        return await self.user_repository.delete(user_id)

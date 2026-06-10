from app.domain.interfaces.repositories.user_repository import UserRepository
from app.domain.enums.role import RoleName


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

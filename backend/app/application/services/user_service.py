from app.domain.interfaces.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: str):
        return await self.user_repository.find_by_id(user_id)

    async def list_users(self):
        return []

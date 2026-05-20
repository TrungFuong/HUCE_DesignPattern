from sqlalchemy import select

from app.application.utils.enum_parser import parse_enum
from app.domain.entities.user import User
from app.domain.enums.role import RoleName
from app.domain.interfaces.repositories.user_repository import UserRepository
from app.infrastructure.database.sqlserver.models.user_model import UserModel


class SqlUserRepository(UserRepository):

    def __init__(self, db_session=None):
        self.db_session = db_session

    async def find_by_email(self, email: str) -> User | None:
        result = await self.db_session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalars().first()
        if model is None:
            return None
        return User(
            id=model.id,
            full_name=model.full_name,
            email=model.email,
            password_hash=model.password_hash,
            role=parse_enum(RoleName, model.role),
            is_active=model.is_active,
            created_at=model.created_at,
        )

    async def find_by_id(self, user_id: str) -> User | None:
        model = await self.db_session.get(UserModel, user_id)
        if model is None:
            return None
        return User(
            id=model.id,
            full_name=model.full_name,
            email=model.email,
            password_hash=model.password_hash,
            role=parse_enum(RoleName, model.role),
            is_active=model.is_active,
            created_at=model.created_at,
        )

    async def save(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            password_hash=user.password_hash,
            role=int(user.role),
            is_active=user.is_active,
            created_at=user.created_at,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return user

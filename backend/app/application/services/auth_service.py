from datetime import datetime, timedelta
import uuid

from app.core.security import hash_password, create_access_token, verify_password
from app.domain.interfaces.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.enums.role import RoleName


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _parse_role(self, role: str | None) -> RoleName:
        if not role:
            return RoleName.FARMER

        role_aliases = {
            "1": RoleName.FARMER,
            "2": RoleName.DISTRIBUTOR,
            "3": RoleName.IMPORTER,
            "4": RoleName.ADMIN,
        }
        normalized_role = role.strip().upper()
        if normalized_role in role_aliases:
            return role_aliases[normalized_role]
        try:
            return RoleName[normalized_role]
        except KeyError as error:
            valid_roles = ", ".join([role.value for role in RoleName])
            raise ValueError(f"Invalid role. Use one of: {valid_roles}") from error

    async def register(self, data):
        existing = await self.user_repository.find_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        password_hash = hash_password(data.password)
        user = User(
            id=str(uuid.uuid4()),
            full_name=data.full_name,
            email=data.email,
            password_hash=password_hash,
            role=self._parse_role(data.role),
            is_active=True,
            created_at=datetime.utcnow(),
        )
        await self.user_repository.save(user)
        expires = datetime.utcnow() + timedelta(minutes=60)
        token = create_access_token({"sub": user.email, "role": user.role.value})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_at": expires,
        }

    async def login(self, data):
        user = await self.user_repository.find_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid credentials")
        expires = datetime.utcnow() + timedelta(minutes=60)
        token = create_access_token({"sub": user.email, "role": user.role.value})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_at": expires,
        }

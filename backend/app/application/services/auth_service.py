from datetime import datetime, timedelta
import uuid

from app.core.security import hash_password, create_access_token, verify_password
from app.domain.interfaces.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.enums.role import RoleName
from app.application.utils.enum_parser import format_enum_options, parse_enum


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _parse_role(self, role: int | str | None) -> RoleName:
        if role is None or role == "":
            return RoleName.FARMER
        try:
            return parse_enum(RoleName, role)
        except (KeyError, ValueError) as error:
            valid_roles = format_enum_options(RoleName)
            raise ValueError(f"Invalid role. Use one of: {valid_roles}") from error

    async def register(self, data):
        self._validate_register_data(data)
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
        token = create_access_token({"sub": user.email, "role": int(user.role)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_at": expires,
        }

    def _validate_register_data(self, data) -> None:
        if not data.full_name.strip():
            raise ValueError("Full name is required")
        if not data.email.strip() or "@" not in data.email:
            raise ValueError("Valid email is required")
        if len(data.password) < 6:
            raise ValueError("Password must be at least 6 characters")

    async def login(self, data):
        user = await self.user_repository.find_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid credentials")
        expires = datetime.utcnow() + timedelta(minutes=60)
        token = create_access_token({"sub": user.email, "role": int(user.role)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_at": expires,
        }

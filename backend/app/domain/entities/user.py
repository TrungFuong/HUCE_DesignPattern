from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.role import RoleName


@dataclass
class User:
    id: str
    full_name: str
    email: str
    password_hash: str
    role: RoleName
    is_active: bool
    created_at: datetime

    def update_info(self, full_name: str | None = None, email: str | None = None, role: RoleName | None = None, is_active: bool | None = None) -> None:
        if full_name is not None:
            self.full_name = full_name
        if email is not None:
            self.email = email
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active

    def change_password(self, new_password_hash: str) -> None:
        self.password_hash = new_password_hash

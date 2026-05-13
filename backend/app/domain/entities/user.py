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

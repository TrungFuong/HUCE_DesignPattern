from pydantic import BaseModel
from typing import Optional

class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None
    is_active: Optional[bool] = None


class CreateUserRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: int

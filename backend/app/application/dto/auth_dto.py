from datetime import datetime
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: int | str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

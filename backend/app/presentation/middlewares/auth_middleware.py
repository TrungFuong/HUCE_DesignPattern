"""JWT authentication dependency used by middleware-style integrations."""

from fastapi import Depends

from app.core.dependencies import get_current_user


async def require_auth(current_user: dict = Depends(get_current_user)) -> dict:
    return current_user

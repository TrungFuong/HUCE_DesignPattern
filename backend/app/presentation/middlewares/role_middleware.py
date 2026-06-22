"""
role_middleware.py — Role-based authorization via FastAPI Depends.

Roles trong hệ thống OCOP:
  1 = FARMER
  2 = TRADER  
  3 = DISTRIBUTOR
  4 = IMPORTER
  5 = ADMIN

Cách dùng trong controller:
    from app.presentation.middlewares.role_middleware import require_role

    @router.post("/admin-only")
    async def admin_endpoint(user=Depends(require_role(5))):  # ADMIN only
        ...

    @router.post("/farmer-or-admin")
    async def farmer_endpoint(user=Depends(require_role(1, 5))):  # FARMER hoặc ADMIN
        ...
"""
from fastapi import Depends, HTTPException

from app.presentation.middlewares.auth_middleware import require_auth

ROLE_NAMES = {
    1: "FARMER",
    2: "TRADER",
    3: "DISTRIBUTOR",
    4: "IMPORTER",
    5: "ADMIN",
}


def require_role(*allowed_roles: int):
    """
    Factory tạo dependency kiểm tra role của user.
    Dùng: Depends(require_role(1, 5)) = chỉ cho FARMER hoặc ADMIN.
    """
    async def role_checker(user: dict = Depends(require_auth)) -> dict:
        user_role = user.get("role")
        if user_role not in allowed_roles:
            allowed_names = [ROLE_NAMES.get(r, str(r)) for r in allowed_roles]
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role(s): {', '.join(allowed_names)}",
            )
        return user
    return role_checker


def require_admin():
    """Shortcut: chỉ cho ADMIN (role=5)."""
    return require_role(5)


def require_farmer_or_admin():
    """Shortcut: FARMER (1) hoặc ADMIN (5)."""
    return require_role(1, 5)

"""Role-based authorization helpers built on the shared JWT auth context."""

from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName


def require_role(*allowed_roles: int):
    return require_roles(*allowed_roles)


def require_admin():
    return require_roles(RoleName.ADMIN)


def require_farmer_or_admin():
    return require_roles(RoleName.FARMER, RoleName.ADMIN)

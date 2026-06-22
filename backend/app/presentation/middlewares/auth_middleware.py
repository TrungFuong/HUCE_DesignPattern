"""
auth_middleware.py — JWT authentication helper via FastAPI Depends + HTTPBearer.

Cách dùng trong controller:
    from app.presentation.middlewares.auth_middleware import require_auth
    
    @router.get("/protected")
    async def my_endpoint(user=Depends(require_auth)):
        return {"user": user}
"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token

_http_bearer = HTTPBearer(auto_error=False)


async def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(_http_bearer),
) -> dict:
    """
    Dependency: xác thực JWT Bearer token.
    Trả về payload dict nếu hợp lệ, raise 401 nếu không.
    Hiển thị ổ khoá 🔒 trong Swagger UI.
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("ocop.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware ghi log mọi HTTP request/response.
    Log format: METHOD path → status_code (duration ms)
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s → %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        # Thêm header thời gian xử lý vào response
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.1f}"
        return response

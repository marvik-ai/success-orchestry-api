import logging
import time

from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger('app.request')

SKIP_PATHS: set[str] = {'/', '/health'}


async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if request.url.path in SKIP_PATHS:
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        '%s %s -> %s %.2fms',
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

import logging
import time

from starlette.requests import Request

logger = logging.getLogger('app.request')

SKIP_PATHS = {'/', '/health'}


async def log_requests(request: Request, call_next):
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

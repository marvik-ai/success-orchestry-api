from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response

from common.config import settings


async def add_version_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    response.headers['X-Version'] = settings.version
    return response

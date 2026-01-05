from starlette.requests import Request

from common.config import settings


async def add_version_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Version"] = settings.version
    return response

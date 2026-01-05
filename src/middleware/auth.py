from starlette.requests import Request
from starlette.responses import JSONResponse

from common.config import settings

PUBLIC_ENDPOINTS = {"/", "/health", "/docs", "/openapi.json", "/redoc"}

def _missing_auth_response() -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": "Forbidden"})

async def check_client_auth(request: Request, call_next):
    if request.url.path in PUBLIC_ENDPOINTS:
        return await call_next(request)

    if not settings.require_client_auth:
        return await call_next(request)

    client = request.headers.get("X-Client-Key")
    secret = request.headers.get("X-Client-Secret")
    if client != settings.client_key or secret != settings.client_secret:
        return _missing_auth_response()

    return await call_next(request)

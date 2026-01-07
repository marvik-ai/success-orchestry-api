from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from common.config import settings
from common.logging_config import configure_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import add_version_header, check_client_auth, log_requests
from router.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup actions
    configure_logging()
    yield
    # Shutdown actions


app = FastAPI(
    title='Success Orchestry API',
    description='Core API for Success Orchestry services.',
    version=settings.version,
    lifespan=lifespan,
)

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)

app.middleware('http')(check_client_auth)
app.middleware('http')(add_version_header)
app.middleware('http')(log_requests)

app.include_router(api_router)


@app.get('/', include_in_schema=False)
def read_root() -> dict[str, str]:
    return {'status': 'API is running'}

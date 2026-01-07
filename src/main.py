from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from common.config import settings
from common.logging_config import configure_logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from middleware import add_version_header, check_client_auth, log_requests
from pydantic import ValidationError
from router.router import router as api_router
from sqlalchemy.exc import IntegrityError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Maneja el ciclo de vida de la aplicación (Startup y Shutdown)."""
    configure_logging()
    yield


app = FastAPI(
    title='Success Orchestry API',
    description='Core API for Success Orchestry services.',
    version=settings.version,
    lifespan=lifespan,
)

# --- Exception Handlers ---


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Captura los raise ValueError de nuestros validadores de SQLModel."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': str(exc)},
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Captura errores de validación estructurales de Pydantic."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={'detail': exc.errors()},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Captura violaciones de integridad en la base de datos (Unique constraints)."""
    # Aquí podrías loguear exc.orig para debug interno si fuera necesario
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={'detail': 'El recurso ya existe o viola una restricción de base de datos.'},
    )


# --- Middleware configuration ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)

# El orden es vital: check_client_auth suele ir primero para proteger el resto
app.middleware('http')(check_client_auth)
app.middleware('http')(add_version_header)
app.middleware('http')(log_requests)

app.include_router(api_router)


@app.get('/', include_in_schema=False)
def read_root() -> dict[str, str]:
    """Endpoint raíz para verificación de estado de la API."""
    return {'status': 'API is running'}

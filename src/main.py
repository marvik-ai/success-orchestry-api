from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from common.config import settings
from common.logging_config import configure_logging
from middleware import add_version_header, check_client_auth, log_requests
from router.router import router as api_router


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
    msg = str(exc.orig).lower()
    if 'unique' in msg:
        detail = 'Ya existe un registro con esos datos (campo duplicado).'
        status_code = status.HTTP_409_CONFLICT
    elif 'foreign key' in msg:
        detail = 'Estás intentando referenciar un registro (como un ID) que no existe.'
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        detail = 'Violación de integridad en la base de datos.'
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(status_code=status_code, content={'detail': detail})


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle general SQLAlchemy errors.

    Captures errors such as syntax errors, lost connections,
    or schema mismatches.
    """
    # En desarrollo es útil ver el error, en producción mejor ocultarlo.
    detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'detail': 'Error interno de base de datos.',
            'technical_details': detail,  # <--- CUIDADO: Solo en desarrollo
        },
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

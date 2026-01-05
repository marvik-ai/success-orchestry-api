from fastapi import FastAPI
from contextlib import asynccontextmanager
from common.database import create_db_and_tables
from router.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from common.logging_config import configure_logging
from common.config import settings
from middleware import add_version_header, check_client_auth, log_requests

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions (replaces startup event)
    configure_logging()
    create_db_and_tables()
    yield
    # Shutdown actions (replaces shutdown event)
    pass

app = FastAPI(
    title="Success Orchestry API",
    description="Core API for Success Orchestry services.",
    version=settings.version,
    lifespan=lifespan,
)
# Add middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
# middleware
app.middleware("http")(check_client_auth)
app.middleware("http")(add_version_header)
app.middleware("http")(log_requests)
# Include routers
app.include_router(api_router)

@app.get("/", include_in_schema=False)
def read_root():
    return {"status": "API is running"}

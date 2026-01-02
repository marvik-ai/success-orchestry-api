from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.Database.database import create_db_and_tables
from app.Controllers import AuthController, ClientController, EmployeeController, RoleController, SeniorityController, CountryController
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions (replaces startup event)
    create_db_and_tables()
    yield
    # Shutdown actions (replaces shutdown event)
    pass

app = FastAPI(lifespan=lifespan)
# Add middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
# Include routers
app.include_router(ClientController.router)
app.include_router(AuthController.router)
app.include_router(EmployeeController.router)
app.include_router(RoleController.router)
app.include_router(SeniorityController.router)
app.include_router(CountryController.router)

@app.get("/")
def read_root():
    return {"status": "API is running"}

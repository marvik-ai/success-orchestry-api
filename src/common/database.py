from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

# 1. Database URL configuration
# If a Docker environment variable is set, use it; otherwise use localhost
from common.config import settings

DATABASE_URL = settings.database_url

# 2. Engine creation
# echo=True prints all SQL queries in the console (useful for debugging)
engine = create_engine(DATABASE_URL, echo=True)

# 3. Function to create tables
# This function reads all models that inherit from SQLModel (like your Employee class)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. Session generator (Dependency Injection)
# Used in controllers with Depends(get_session)
def get_session():
    with Session(engine) as session:
        yield session

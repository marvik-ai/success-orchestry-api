from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from common.config import settings


# 1. Database URL configuration
DATABASE_URL = settings.database_url

# 2. Engine creation
engine = create_engine(DATABASE_URL, echo=True)


# 3. Function to create tables
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


# 4. Session generator (Dependency Injection)
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

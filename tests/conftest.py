import os
import sys
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from common.database import get_session
from main import app


SRC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

TEST_DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)


@pytest.fixture(name='session')
def session_fixture() -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name='client')
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

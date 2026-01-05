import os

from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["APP_VERSION"] = "test"

from main import app


def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

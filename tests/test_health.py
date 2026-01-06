import os

from fastapi.testclient import TestClient
from main import app

os.environ['DATABASE_URL'] = 'sqlite://'
os.environ['APP_VERSION'] = 'test'


def test_health_check() -> None:
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

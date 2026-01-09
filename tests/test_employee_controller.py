from collections.abc import Generator
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from dependencies import get_employees_services
from main import app
from services.employee_service import EmployeeService


@pytest.fixture
def mock_service() -> Mock:
    return Mock(spec=EmployeeService)


@pytest.fixture
def client_with_mocked_service(
    client: TestClient, mock_service: Mock
) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_employees_services] = lambda: mock_service
    yield client
    app.dependency_overrides.pop(get_employees_services, None)


def test_router_delete_employee_success(
    client_with_mocked_service: TestClient, mock_service: Mock
) -> None:
    # --- ARRANGE ---
    emp_id = uuid4()
    mock_service.get_employee_by_id.return_value = Mock()
    mock_service._check_active_projects.return_value = False
    mock_service.delete_employee.return_value = None

    # --- ACT ---
    response = client_with_mocked_service.delete(f'Employees/{emp_id}')

    # --- ASSERT ---
    assert response.status_code == status.HTTP_204_NO_CONTENT

    mock_service.delete_employee.assert_called_once()

    args, _ = mock_service.delete_employee.call_args
    assert args[0] == emp_id


def test_router_delete_employee_not_found(
    client_with_mocked_service: TestClient, mock_service: Mock
) -> None:
    # --- ARRANGE ---
    emp_id = uuid4()

    mock_service.get_employee_by_id.return_value = None

    # --- ACT ---
    response = client_with_mocked_service.delete(f'Employees/{emp_id}')

    # --- ASSERT ---
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Employee not found or already deleted'
    mock_service.delete_employee.assert_not_called()


def test_router_delete_employee_invalid_uuid(
    client_with_mocked_service: TestClient, mock_service: Mock
) -> None:
    """Prueba que FastAPI valida el tipo de dato antes de llamar al servicio."""
    # --- ARRANGE ---
    invalid_id = '123-no-es-uuid'

    # --- ACT ---
    response = client_with_mocked_service.delete(f'Employees/{invalid_id}')

    # --- ASSERT ---
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    mock_service.delete_employee.assert_not_called()

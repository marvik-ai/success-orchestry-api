from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from models.employee_model import Employee, EmployeeStatus
from services.employee_service import EmployeeService


@pytest.fixture
def mock_repo() -> Mock:
    return Mock()


@pytest.fixture
def service(mock_repo: Mock) -> EmployeeService:
    return EmployeeService(emp_repo=mock_repo)


def test_delete_employee_success(service: EmployeeService, mock_repo: Mock) -> None:
    # --- ARRANGE ---
    emp_id = uuid4()
    mock_employee = Employee(id=emp_id, status=EmployeeStatus.ACTIVE)
    mock_repo.get_by_id.return_value = mock_employee
    with patch.object(service, '_check_active_projects', return_value=False):
        service.delete_employee(emp_id)

    # --- ASSERT ---
    mock_repo.soft_delete.assert_called_once_with(mock_employee)

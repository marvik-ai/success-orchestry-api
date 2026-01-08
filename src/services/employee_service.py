from typing import Any
from uuid import UUID

from fastapi import HTTPException, status

from models.employee_model import Employee, EmployeeCreate
from repositories.employee_repository import EmployeeRepositoryClass


class EmployeeService:
    def __init__(self, emp_repo: EmployeeRepositoryClass) -> None:
        self.emp_repo = emp_repo

    def update(self, employee_id: int, data: dict[str, Any]) -> Employee:
        updated_employee = self.emp_repo.update_employee(employee_id, data)

        if updated_employee is None:
            raise HTTPException(status_code=404, detail='Employee not found')

        return updated_employee

    def search_employees(self, name: str | None) -> list[Employee]:
        """Busca empleados filtrando por nombre."""
        # Al asegurar que el repo devuelve list[Employee], MyPy estará satisfecho
        return self.emp_repo.get_filtered_employees(name)

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        return self.emp_repo.create_employee(employee)

    def _check_active_projects(self, employee_id: UUID) -> bool:
        """TODO: This function should return true if the employee has any active project assignments."""
        return False

    def delete_employee(self, employee_id: UUID) -> None:
        employee = self.emp_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Employee not found or already deleted',
            )
        if self._check_active_projects(employee_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Cannot delete employee with active project assignments.',
            )
        self.emp_repo.soft_delete(employee)

from typing import Any, Literal
from uuid import UUID

from fastapi import HTTPException

from models.employee_model import (
    Employee,
    EmployeeCreate,
    EmployeePaginationResponse,
    EmployeePublicResponse,
    EmployeeStatus,
)
from repositories.employee_repository import EmployeeRepositoryClass


class EmployeeService:
    def __init__(self, emp_repo: EmployeeRepositoryClass) -> None:
        self.emp_repo = emp_repo

    def update(self, employee_id: int, data: dict[str, Any]) -> Employee:
        updated_employee = self.emp_repo.update_employee(employee_id, data)

        if updated_employee is None:
            raise HTTPException(status_code=404, detail='Employee not found')

        return updated_employee

    # Search and get
    def search_employees(
        self,
        name: str | None = None,
        status: EmployeeStatus | None = None,
        role_id: UUID | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str = 'created_at',
        order: Literal['asc', 'desc'] = 'desc',
    ) -> EmployeePaginationResponse:
        """Fetch employees and return a structured pagination response."""
        # Repository now returns flat dictionaries
        safe_page = page if page > 0 else 1
        items, total = self.emp_repo.get_filtered_employees(
            name=name,
            status=status,
            role_id=role_id,
            search=search,
            page=safe_page,
            limit=limit,
            sort_by=sort_by,
            order=order,
        )

        return EmployeePaginationResponse(items=items, total=total, page=page, limit=limit)

    def get_employee_by_id(self, employee_id: UUID) -> EmployeePublicResponse | None:
        employee_dict = self.emp_repo.get_employee_by_id(employee_id)
        if not employee_dict:
            return None
        return employee_dict

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        return self.emp_repo.create_employee(employee)

    def _check_active_projects(self, employee_id: UUID) -> bool:
        """TODO: This function should return true if the employee has any active project assignments."""
        return False

    def delete_employee(self, employee_id: UUID) -> None:
        employee = self.emp_repo.get_by_id(employee_id)
        if not employee:
            return
        self.emp_repo.soft_delete(employee)

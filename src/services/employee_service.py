from typing import Any

from fastapi import HTTPException

from models.employee_model import Employee, EmployeeCreate, EmployeePaginationResponse
from repositories.employee_repository import EmployeeRepositoryClass


class EmployeeService:
    def __init__(self, emp_repo: EmployeeRepositoryClass) -> None:
        self.emp_repo = emp_repo

    def update(self, employee_id: int, data: dict[str, Any]) -> Employee:
        updated_employee = self.emp_repo.update_employee(employee_id, data)

        if updated_employee is None:
            raise HTTPException(status_code=404, detail='Employee not found')

        return updated_employee

    def search_employees(self, **kwargs: Any) -> EmployeePaginationResponse:
        """Busca empleados y devuelve un objeto estructurado de paginación."""
        # El repo sigue devolviendo la tupla (datos, total)
        items, total = self.emp_repo.get_filtered_employees(**kwargs)

        # Retornamos el modelo de Pydantic explícitamente
        return EmployeePaginationResponse(
            items=items, total=total, page=kwargs.get('page', 1), limit=kwargs.get('limit', 10)
        )

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        return self.emp_repo.create_employee(employee)

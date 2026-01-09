from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from dependencies import EmployeeService, get_employees_services
from models.employee_model import (
    Employee,
    EmployeeCreate,
    EmployeePaginationResponse,
    EmployeePublicResponse,
    EmployeeStatus,
)


router = APIRouter(prefix='/Employees', tags=['Employee'])


@router.patch('/{employee_id}')
def update_employee(
    employee_id: int,
    employee_data: Employee,
    service: EmployeeService = Depends(get_employees_services),
) -> Employee:
    """Actualiza los datos de un empleado de forma parcial.

    Utiliza model_dump con exclude_unset para asegurar que solo los campos
    enviados en el cuerpo de la petición sean procesados por el servicio.
    """
    return service.update(employee_id, employee_data.model_dump(exclude_unset=True))


@router.get('/{employee_id}', response_model=EmployeePublicResponse)
def get_employee(
    employee_id: UUID,
    service: EmployeeService = Depends(get_employees_services),
) -> EmployeePublicResponse:
    return service.get_employee_by_id(employee_id)


@router.get('/', response_model=EmployeePaginationResponse)
def get_employees(
    service: EmployeeService = Depends(get_employees_services),
    name: str | None = Query(None),
    status: EmployeeStatus | None = Query(None),
    role_id: UUID | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query('created_at'),
    order: Literal['asc', 'desc'] = Query('desc'),
) -> EmployeePaginationResponse:
    # Ensure page is at least 1

    return service.search_employees(
        name=name,
        status=status,
        role_id=role_id,
        search=search,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


@router.post('/')
def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService = Depends(get_employees_services),
) -> Employee:
    """Registra un nuevo empleado en el sistema.

    Valida los datos de entrada mediante el esquema EmployeeCreate y delega
    la persistencia al servicio de empleados.
    """
    emp_log = employee.name if hasattr(employee, 'name') else employee
    print(f'Creating employee: {emp_log}')
    return service.create_employee(employee)

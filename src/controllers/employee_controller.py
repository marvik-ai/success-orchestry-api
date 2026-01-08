from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from dependencies import EmployeeService, get_employees_services
from models.employee_model import (
    Employee,
    EmployeeCreate,
    EmployeePaginationResponse,
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


@router.get('/', response_model=EmployeePaginationResponse)
def get_employees(
    service: EmployeeService = Depends(get_employees_services),
    name: str | None = Query(None, description='Employee name'),
    status: EmployeeStatus | None = Query(None, description='Filter by status'),
    role_id: UUID | None = Query(None, description='Filter by role ID'),
    search: str | None = Query(None, description='Partial search (name, code, etc.)'),
    # Pagination: default limit 10
    page: int = Query(1, description='Page number'),
    limit: int = Query(10, ge=1, le=100, description='Records per page'),
    # Sorting
    sort_by: str = Query('created_at', description='Field to sort by'),
    order: Literal['asc', 'desc'] = Query('desc', description='Sort direction'),
) -> list[Employee]:
    # Debug log to verify all filters are received
    print(f'FILTERS: name={name}, status={status}, search={search}, page={page}, limit={limit}')

    # Pass ALL parameters to the service
    return list(
        service.search_employees(
            name=name,
            status=status,
            role_id=role_id,
            search=search,
            page=page,
            limit=limit,
            sort_by=sort_by,
            order=order,
        )
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

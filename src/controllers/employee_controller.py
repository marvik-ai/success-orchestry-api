from fastapi import APIRouter, Depends, Query

from dependencies import EmployeeService, get_employees_services
from models.employee_model import Employee, EmployeeCreate


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


@router.get('/')
def get_employees(
    service: EmployeeService = Depends(get_employees_services),
    name: str | None = Query(None, description='Partial search by name'),
) -> list[Employee]:  # FastAPI prefiere list para la generación de esquemas JSON
    print(f'RECEIVED FILTERS: name={name}')
    return list(service.search_employees(name))


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

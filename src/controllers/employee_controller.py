from fastapi import APIRouter, Depends, Query

from dependencies import EmployeeService, get_employees_services
from models.employee_model import Employee, EmployeeCreate

router = APIRouter(prefix='/Employees', tags=['Employee'])


@router.patch('/{employee_id}')
def update_employee(
    employee_id: int,
    employee_data: Employee,
    service: EmployeeService = Depends(get_employees_services),
):
    return service.update(employee_id, employee_data.model_dump(exclude_unset=True))


@router.get('/')
def get_employees(
    name: str | None = Query(None, description='Partial search by name'),
    service: EmployeeService = Depends(get_employees_services),
):
    print(f'RECEIVED FILTERS: name={name}')
    return service.search_employees(name)


@router.post('/')
def create_employee(
    employee: EmployeeCreate, service: EmployeeService = Depends(get_employees_services)
):
    print(f'Employee: {employee}')
    return service.create_employee(employee)

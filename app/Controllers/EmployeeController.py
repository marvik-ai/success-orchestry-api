from fastapi import APIRouter, Depends, Query
from app.dependencies import get_employees_services, EmployeeService
from app.Models.EmployeeModel import Employee, EmployeeCreate

from typing import Optional

router = APIRouter(prefix="/Employees", tags=["Employee"])

@router.patch("/{employee_id}")
def update_employee(
    employee_id: int, 
    employee_data: Employee, 
    service : EmployeeService = Depends(get_employees_services)
):
    return service.update(employee_id, employee_data.model_dump(exclude_unset=True))

@router.get("/")
def get_employees(
    name: Optional[str] = Query(None, description="Partial search by name"),
    country_id: Optional[int] = Query(None),
    seniority_id: Optional[int] = Query(None),
    role_id: Optional[int] = Query(None),
    service : EmployeeService = Depends(get_employees_services)
):
    print(f"RECEIVED FILTERS: name={name}, country={country_id}, role={role_id}")
    return service.search_employees(name, country_id, seniority_id, role_id)

@router.post("/")
def create_employee(
    employee : EmployeeCreate,
    service : EmployeeService = Depends(get_employees_services)
):
    print(f"Employee: {employee}")
    return service.create_employee(employee)

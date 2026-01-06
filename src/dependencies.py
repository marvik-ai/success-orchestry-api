from common.database import get_session
from fastapi import Depends
from repositories.employee_repository import EmployeeRepositoryClass
from services.employee_service import EmployeeService
from sqlmodel import Session


# --- Dependencies ---
def get_db(session: Session = Depends(get_session)):
    return session


# --- repositories ---
def get_employees_repo(session: Session = Depends(get_session)):
    return EmployeeRepositoryClass(session)


# --- services ---
def get_employees_services(
    emp_repo: EmployeeRepositoryClass = Depends(get_employees_repo),
) -> EmployeeService:
    return EmployeeService(emp_repo)

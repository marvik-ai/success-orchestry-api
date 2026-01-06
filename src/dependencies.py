from fastapi import Depends
from repositories.employee_repository import EmployeeRepositoryClass

# Usamos el alias redundante para exportar explícitamente a MyPy
from services.employee_service import EmployeeService as EmployeeService
from sqlmodel import Session

from src.common.database import get_session


# --- Dependencies ---
def get_db(session: Session = Depends(get_session)) -> Session:
    return session


# --- repositories ---
def get_employees_repo(
    session: Session = Depends(get_session),
) -> EmployeeRepositoryClass:
    return EmployeeRepositoryClass(session)


# --- services ---
def get_employees_services(
    emp_repo: EmployeeRepositoryClass = Depends(get_employees_repo),
) -> EmployeeService:
    return EmployeeService(emp_repo)

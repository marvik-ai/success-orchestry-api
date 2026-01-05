from fastapi import Depends
from sqlmodel import Session

from common.database import get_session
from repositories.EmployeeRepository import EmployeeRepositoryClass
from services.EmployeeService import EmployeeService

# --- Dependencies ---
def get_db(session: Session = Depends(get_session)):
    return session

# --- repositories ---

def get_employees_repo(session: Session = Depends(get_session)):
    return EmployeeRepositoryClass(session)

# --- services ---

def get_employees_services(emp_repo: EmployeeRepositoryClass = Depends(get_employees_repo)) -> EmployeeService:
    return EmployeeService(emp_repo)

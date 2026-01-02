from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.Database.database import get_session
from app.Database.Repositories.EmployeeRepository import EmployeeRepositoryClass
from app.Database.Repositories.ClientRepository import ClientRepositoryClass
from app.Database.Repositories.SeniorityRepository import SeniorityRepositoryClass
from app.Database.Repositories.RolesRepository import RoleRepositoryClass
from app.Database.Repositories.CountryRepository import CountryRepositoryClass
from app.Database.Repositories.UserRepository import UserRepository

from app.Services.EmployeeService import EmployeeService
from app.Services.ClientService import ClientService
from app.Services.SeniorityService import SeniorityService
from app.Services.RoleService import RoleService
from app.Services.CountryService import CountryService
from app.Services.AuthService import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Dependencies ---

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session: Session = Depends(get_session)
):
    user = AuthService.get_user_from_token(session, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or user not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_db(session: Session = Depends(get_session)):
    return session

# --- Repositories ---

def get_employees_repo(session: Session = Depends(get_session)):
    return EmployeeRepositoryClass(session)

def get_clients_repo(session: Session = Depends(get_session)):
    return ClientRepositoryClass(session)

def get_countries_repo(session: Session = Depends(get_session)):
    return CountryRepositoryClass(session)

def get_roles_repo(session: Session = Depends(get_session)):
    return RoleRepositoryClass(session)

def get_seniorities_repo(session: Session = Depends(get_session)):
    return SeniorityRepositoryClass(session)

def get_users_repo(session: Session = Depends(get_session)):
    return UserRepository(session)

# --- Services ---

def get_employees_services(emp_repo: EmployeeRepositoryClass = Depends(get_employees_repo)) -> EmployeeService:
    return EmployeeService(emp_repo)

def get_clients_services(cli_repo: ClientRepositoryClass = Depends(get_clients_repo)) -> ClientService:
    return ClientService(cli_repo)

def get_roles_services(role_repo: RoleRepositoryClass = Depends(get_roles_repo)) -> RoleService:
    return RoleService(role_repo)

def get_seniorities_services(seniority_repo: SeniorityRepositoryClass = Depends(get_seniorities_repo)) -> SeniorityService:
    return SeniorityService(seniority_repo)

def get_countries_services(country_repo: CountryRepositoryClass = Depends(get_countries_repo)) -> CountryService:
    return CountryService(country_repo)

def get_auth_services(
    user_repo: UserRepository = Depends(get_users_repo),
    emp_repo: EmployeeRepositoryClass = Depends(get_employees_repo)
) -> AuthService:
    return AuthService(user_repo, emp_repo)

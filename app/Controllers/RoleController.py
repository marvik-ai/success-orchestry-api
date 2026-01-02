from fastapi import APIRouter, Depends, HTTPException
from app.Models.RoleModel import Role, RoleCreate
from app.dependencies import get_roles_services, RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=Role)
def create_role(role: RoleCreate, service: RoleService = Depends(get_roles_services)):
    return service.add(role)

@router.get("/", response_model=list[Role])
def list_roles(service: RoleService = Depends(get_roles_services)):
    return service.get_all()

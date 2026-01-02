from fastapi import APIRouter, Depends, HTTPException
from app.Models.SeniorityModel import Seniority, SeniorityCreate
from app.dependencies import get_seniorities_services, SeniorityService

router = APIRouter(prefix="/seniorities", tags=["Seniorities"])

@router.post("/", response_model=SeniorityCreate)
def create_seniority(seniority: SeniorityCreate, service: SeniorityService = Depends(get_seniorities_services)):
    return service.add(seniority)

@router.get("/", response_model=list[Seniority])
def list_seniorities(service: SeniorityService = Depends(get_seniorities_services)):
    return service.get_all()

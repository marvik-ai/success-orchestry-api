from fastapi import APIRouter, Depends, HTTPException
from app.Models.CountryModel import CountryCreate, Country
from app.dependencies import get_countries_services, CountryService

router = APIRouter(prefix="/countries", tags=["Countries"])

@router.post("/", response_model=Country)
def create_country(country: CountryCreate, service: CountryService = Depends(get_countries_services)):
    return service.add(country)

@router.get("/", response_model=list[Country])
def list_countries(service: CountryService = Depends(get_countries_services)):
    return service.get_all()

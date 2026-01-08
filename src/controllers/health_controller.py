from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from dependencies import get_db
from services.health_service import HealthService


router = APIRouter(tags=['Health'])


class HealthResponse(BaseModel):
    status: str


@router.get(
    '/health',
    response_model=HealthResponse,
    summary='Health check',
    description='Checks database connectivity and returns API health status.',
)
def health_check(session: Session = Depends(get_db)) -> dict[str, str]:
    service = HealthService(session)
    try:
        return service.check()
    except Exception as err:
        raise HTTPException(
            status_code=503,
            detail='Database unavailable',
        ) from err

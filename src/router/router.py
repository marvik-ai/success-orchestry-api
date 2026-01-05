from fastapi import APIRouter

from controllers import (
    EmployeeController,
    HealthController,
)

router = APIRouter()

router.include_router(EmployeeController.router, include_in_schema=False)
router.include_router(HealthController.router)

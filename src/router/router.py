from fastapi import APIRouter

from controllers import (
    employee_controller,
    health_controller,
)

router = APIRouter()

router.include_router(employee_controller.router, include_in_schema=False)
router.include_router(health_controller.router)

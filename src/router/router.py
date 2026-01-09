from fastapi import APIRouter

from controllers import (
    employee_controller,
    health_controller,
)


router = APIRouter()

router.include_router(employee_controller.router, tags=['Employees'])
router.include_router(health_controller.router)

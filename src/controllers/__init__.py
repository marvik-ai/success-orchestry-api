from controllers.EmployeeController import router as employee_router
from controllers.HealthController import router as health_router

__all__ = [
    "employee_router",
    "health_router",
]

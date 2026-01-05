from models.EmployeeModel import Employee, EmployeeCreate
from repositories.EmployeeRepository import EmployeeRepositoryClass

class EmployeeService:
    def __init__(self, emp_repo: EmployeeRepositoryClass):
        self.emp_repo = emp_repo

    def update(self, employee_id: int, data: dict):
        updated_employee = self.emp_repo.update_employee(employee_id, data)
        return updated_employee

    def search_employees(self, name):
        return self.emp_repo.get_filtered_employees(name)

    def create_employee(self, employee: EmployeeCreate):
        created_employee = self.emp_repo.create_employee(employee)
        return created_employee

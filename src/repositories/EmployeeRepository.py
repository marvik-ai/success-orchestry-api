from sqlmodel import Session, select
from models.EmployeeModel import Employee, EmployeeCreate

class EmployeeRepositoryClass:
    def __init__(self, session: Session):
        self.session = session

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        db_client = Employee.model_validate(employee)
        self.session.add(db_client)
        self.session.commit()
        self.session.refresh(db_client)
        return db_client

    def update_employee(self, employee_id: int, update_data: dict) -> Employee:
        db_employee = self.session.get(Employee, employee_id)
        if not db_employee:
            return None
        
        # Update only fields present in the dictionary
        for key, value in update_data.items():
            setattr(db_employee, key, value)            
        self.session.add(db_employee)
        self.session.commit()
        self.session.refresh(db_employee)
        return db_employee

    def get_filtered_employees(
        self,
        name: str | None = None,
    ):
        query = select(Employee)

        if name and name.strip():
            query = query.where(Employee.name.ilike(f"%{name.strip()}%"))

        return self.session.exec(query).all()

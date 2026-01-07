from typing import Any, cast

from sqlmodel import Session, col, select

from models.employee_model import Employee, EmployeeCreate


class EmployeeRepositoryClass:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        db_client = Employee.model_validate(employee)
        self.session.add(db_client)
        self.session.commit()
        self.session.refresh(db_client)
        return db_client

    def update_employee(self, employee_id: int, update_data: dict[str, Any]) -> Employee | None:
        db_employee = self.session.get(Employee, employee_id)
        if not db_employee:
            return None

        for key, value in update_data.items():
            setattr(db_employee, key, value)

        self.session.add(db_employee)
        self.session.commit()
        self.session.refresh(db_employee)
        return db_employee

    def get_filtered_employees(self, name: str | None = None) -> list[Employee]:
        query = select(Employee)

        if name and name.strip():
            query = query.where(col(Employee.name).ilike(f'%{name.strip()}%'))

        # Ejecutamos y convertimos explícitamente a lista de Employee
        results = self.session.exec(query).all()
        return cast(list[Employee], results)

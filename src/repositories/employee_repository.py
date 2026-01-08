from typing import Any, cast

from sqlmodel import Session, col, select

from models.employee_model import (
    Employee,
    EmployeeBase,
    EmployeeCreate,
    EmployeePersonalInfo,
    EmployeePersonalInfoBase,
)


class EmployeeRepositoryClass:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_employee(self, employee_in: EmployeeCreate) -> Employee:
        # 1. Extraer campos de Información Personal
        # Usamos el esquema base para saber qué llaves extraer
        personal_fields = EmployeePersonalInfoBase.model_fields.keys()
        personal_data = employee_in.model_dump(include=set(personal_fields))
        db_personal_info = EmployeePersonalInfo(**personal_data)

        # 2. Extraer campos de la tabla Employee
        # Extraemos solo lo que pertenece a EmployeeBase
        employee_fields = EmployeeBase.model_fields.keys()
        main_data = employee_in.model_dump(include=set(employee_fields))

        # 3. Instanciar el objeto principal y vincular la relación
        db_employee = Employee(**main_data)
        db_employee.personal_info = db_personal_info

        # 4. Persistir en la DB
        try:
            self.session.add(db_employee)
            self.session.commit()
            self.session.refresh(db_employee)
            return db_employee
        except Exception as e:
            self.session.rollback()
            raise e

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

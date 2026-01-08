from typing import Any, Literal, cast
from uuid import UUID

from sqlalchemy import asc, desc, func, or_
from sqlmodel import Session, col, select

from models.employee_model import (
    Employee,
    EmployeeBase,
    EmployeeCreate,
    EmployeePersonalInfo,
    EmployeePersonalInfoBase,
    EmployeeStatus,
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

    def get_filtered_employees(
        self,
        name: str | None = None,
        status: EmployeeStatus | None = None,
        role_id: UUID | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str = 'created_at',
        order: Literal['asc', 'desc'] = 'desc',
    ) -> tuple[list[Employee], int]:
        # 1. Base query with JOIN (needed to filter by personal info)
        base_query = select(Employee).join(EmployeePersonalInfo)

        # 2. Apply filters (exactly the same for count and data)
        if status:
            base_query = base_query.where(Employee.status == status)

        if name and name.strip():
            search_name = f'%{name.strip()}%'
            base_query = base_query.where(
                or_(
                    col(EmployeePersonalInfo.first_name).ilike(search_name),
                    col(EmployeePersonalInfo.last_name).ilike(search_name),
                )
            )

        if search and search.strip():
            s = f'%{search.strip()}%'
            base_query = base_query.where(
                or_(
                    col(Employee.employee_code).ilike(s),
                    col(EmployeePersonalInfo.first_name).ilike(s),
                    col(EmployeePersonalInfo.last_name).ilike(s),
                    col(EmployeePersonalInfo.personal_email).ilike(s),
                )
            )

        # 3. Get the TOTAL number of records matching the filters
        count_statement = select(func.count()).select_from(base_query.subquery())
        total = self.session.exec(count_statement).one()

        # 4. Apply sorting
        # Check if the column exists in Employee; fallback to created_at
        sort_column = getattr(Employee, sort_by, Employee.created_at)
        if order == 'desc':
            base_query = base_query.order_by(desc(sort_column))
        else:
            base_query = base_query.order_by(asc(sort_column))

        # 5. Apply pagination
        offset_value = (page - 1) * limit
        data_query = base_query.offset(offset_value).limit(limit)

        # 6. Execute query
        results = self.session.exec(data_query).all()

        return cast(list[Employee], results), total

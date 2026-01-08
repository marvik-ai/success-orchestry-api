from typing import Any, Literal
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

    def get_employee_by_id(self, employee_id: UUID) -> dict[str, Any] | None:
        # Realizamos el JOIN para obtener ambas partes de la información en una sola consulta
        statement = (
            select(Employee, EmployeePersonalInfo)
            .join(EmployeePersonalInfo)
            .where(Employee.id == employee_id)
        )

        result = self.session.exec(statement).first()

        if not result:
            return None

        emp, info = result
        # Aplanamos: Los campos de 'info' (first_name, etc) y 'emp' (employee_code, id)
        # se mezclan en un único diccionario.
        return {**info.model_dump(), **emp.model_dump()}

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
    ) -> tuple[list[dict[str, Any]], int]:
        # 1. Base query fetching both tables to flatten later
        base_query = select(Employee, EmployeePersonalInfo).join(EmployeePersonalInfo)

        # 2. Apply filters
        if status:
            base_query = base_query.where(Employee.status == status)

        if name and name.strip():
            clean_name = f'%{name.strip()}%'
            base_query = base_query.where(
                or_(
                    col(EmployeePersonalInfo.first_name).ilike(clean_name),
                    col(EmployeePersonalInfo.last_name).ilike(clean_name),
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

        # 3. Get total count using a subquery
        count_stmt = select(func.count()).select_from(base_query.subquery())
        total = self.session.exec(count_stmt).one()

        # 4. Apply sorting
        sort_col = getattr(Employee, sort_by, Employee.created_at)
        if order == 'desc':
            base_query = base_query.order_by(desc(sort_col))
        else:
            base_query = base_query.order_by(asc(sort_col))

        # 5. Execute with pagination
        offset_value = (page - 1) * limit
        results = self.session.exec(base_query.offset(offset_value).limit(limit)).all()

        # 6. Flatten the results: Combine Employee and PersonalInfo into one dict
        flattened_items = []
        for emp, info in results:
            # Merging dictionaries: info fields + emp fields (emp.id overrides info.id)
            merged_data = {**info.model_dump(), **emp.model_dump()}
            flattened_items.append(merged_data)

        return flattened_items, total

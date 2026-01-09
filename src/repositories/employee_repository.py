from datetime import UTC, datetime
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
    EmployeePublicResponse,
    EmployeeStatus,
)


class EmployeeRepositoryClass:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_employee(self, employee_in: EmployeeCreate) -> Employee:
        personal_fields = EmployeePersonalInfoBase.model_fields.keys()
        personal_data = employee_in.model_dump(include=set(personal_fields))
        db_personal_info = EmployeePersonalInfo(**personal_data)

        employee_fields = EmployeeBase.model_fields.keys()
        main_data = employee_in.model_dump(include=set(employee_fields))

        db_employee = Employee(**main_data)
        db_employee.personal_info = db_personal_info

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

    def get_employee_by_id(self, employee_id: UUID) -> EmployeePublicResponse | None:
        statement = (
            select(Employee, EmployeePersonalInfo)
            .join(EmployeePersonalInfo)
            .where(Employee.id == employee_id)
        )

        result = self.session.exec(statement).first()

        if not result:
            return None

        emp, info = result

        combined_data = {**info.model_dump(), **emp.model_dump()}

        return EmployeePublicResponse.model_validate(combined_data)

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
    ) -> tuple[list[EmployeePublicResponse], int]:
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
        sort_map = {
            'created_at': Employee.created_at,
            'updated_at': Employee.updated_at,
            'employee_code': Employee.employee_code,
            'status': Employee.status,
            'first_name': EmployeePersonalInfo.first_name,
            'last_name': EmployeePersonalInfo.last_name,
            'personal_email': EmployeePersonalInfo.personal_email,
        }
        sort_col = sort_map.get(sort_by, Employee.created_at)

        if order == 'desc':
            base_query = base_query.order_by(desc(col(sort_col)))
        else:
            base_query = base_query.order_by(asc(col(sort_col)))

        # 5. Execute with pagination
        offset_value = (page - 1) * limit
        results = self.session.exec(base_query.offset(offset_value).limit(limit)).all()

        response_items = []
        for emp, info in results:
            # Merging dictionaries
            merged_data = {**info.model_dump(), **emp.model_dump()}
            response_obj = EmployeePublicResponse.model_validate(merged_data)
            response_items.append(response_obj)

        return response_items, total

    def get_by_id(self, employee_id: UUID) -> Employee | None:
        statement = select(Employee).where(
            Employee.id == employee_id, col(Employee.deleted_at).is_(None)
        )
        return self.session.exec(statement).first()

    def soft_delete(self, employee: Employee) -> Employee:
        employee.status = EmployeeStatus.TERMINATED
        employee.deleted_at = datetime.now(UTC)

        if employee.personal_info:
            self.session.delete(employee.personal_info)

        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

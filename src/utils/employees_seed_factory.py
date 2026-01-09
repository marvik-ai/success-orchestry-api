import random
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Generic, TypeVar  # Agregado Generic

# Runtime imports
from polyfactory import Use
from sqlmodel import Session, SQLModel

from common.database import engine
from models.employee_model import (
    Employee,
    EmployeeFinancialInfo,
    EmployeePersonalInfo,
    EmployeeStatus,
)


T = TypeVar('T')

if TYPE_CHECKING:
    # Usamos la sintaxis tradicional para que Mypy no falle.
    class ModelFactory(Generic[T]):  # noqa: UP046
        __model__: type[T]
        __faker__: Any

        @classmethod
        def build(cls, **kwargs: Any) -> T: ...

    def post_generated(func: Any) -> Any: ...
else:
    from polyfactory.decorators import post_generated
    from polyfactory.factories.pydantic_factory import ModelFactory


class EmployeeFactory(ModelFactory[Employee]):
    __model__ = Employee
    employee_code = Use(lambda: EmployeeFactory.__faker__.unique.bothify(text='???-###').upper())
    status = Use(lambda: random.choice(list(EmployeeStatus)))

    @post_generated
    @classmethod
    def deleted_at(cls, status: EmployeeStatus) -> datetime | None:
        if status == EmployeeStatus.TERMINATED:
            return cls.__faker__.date_time_between(start_date='-2y', end_date='now', tzinfo=UTC)
        return None


class EmployeePersonalInfoFactory(ModelFactory[EmployeePersonalInfo]):
    __model__ = EmployeePersonalInfo
    personal_email = Use(lambda: EmployeePersonalInfoFactory.__faker__.unique.email())
    document_number = Use(
        lambda: EmployeePersonalInfoFactory.__faker__.unique.numerify(text='##########')
    )
    phone = Use(lambda: EmployeePersonalInfoFactory.__faker__.unique.phone_number())
    first_name = Use(lambda: EmployeePersonalInfoFactory.__faker__.first_name())
    last_name = Use(lambda: EmployeePersonalInfoFactory.__faker__.last_name())


class EmployeeFinancialInfoFactory(ModelFactory[EmployeeFinancialInfo]):
    __model__ = EmployeeFinancialInfo
    salary_amount = Use(lambda: Decimal(random.randint(2000, 8000)))
    company_cost_amount = Use(lambda: Decimal(random.randint(2500, 9000)))
    salary_currency_id = Use(uuid.uuid4)
    effective_from = Use(
        lambda: EmployeeFinancialInfoFactory.__faker__.date_between(
            start_date='-1y', end_date='today'
        )
    )


def seed_employees(n: int = 10) -> None:
    """Explicitly exported function for seed.py."""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print(f'🌱 Generating {n} employees...')
        for _ in range(n):
            employee: Employee = EmployeeFactory.build()
            session.add(employee)
            session.flush()

            session.add(EmployeePersonalInfoFactory.build(employee_id=employee.id))
            session.add(EmployeeFinancialInfoFactory.build(employee_id=employee.id))

        session.commit()
        print('✨ Database seed complete.')

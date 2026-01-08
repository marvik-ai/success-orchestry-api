import random
from decimal import Decimal

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlmodel import Session, SQLModel

from common.database import engine
from models.employee_model import (
    Employee,
    EmployeeFinancialInfo,
    EmployeePersonalInfo,
    EmployeeStatus,
)


class EmployeeFactory(ModelFactory[Employee]):  # type: ignore[misc]
    __model__ = Employee
    status = Use(lambda: random.choice(list(EmployeeStatus)))


class EmployeePersonalInfoFactory(ModelFactory[EmployeePersonalInfo]):  # type: ignore[misc]
    __model__ = EmployeePersonalInfo

    personal_email = Use(ModelFactory.__faker__.email)
    first_name = Use(ModelFactory.__faker__.first_name)
    last_name = Use(ModelFactory.__faker__.last_name)
    city = Use(ModelFactory.__faker__.city)
    address = Use(ModelFactory.__faker__.address)
    __set_relationships__ = True


class EmployeeFinancialInfoFactory(ModelFactory[EmployeeFinancialInfo]):  # type: ignore[misc]
    __model__ = EmployeeFinancialInfo

    salary_amount = Use(lambda: Decimal(random.randint(2000, 8000)))
    company_cost_amount = Use(lambda: Decimal(random.randint(2500, 9000)))


def seed_employees(n: int = 10) -> None:
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print(f'🌱 Iniciando seed de {n} empleados completos...')

        for _ in range(n):
            employee = EmployeeFactory.build()

            session.add(employee)
            session.flush()
            personal_info = EmployeePersonalInfoFactory.build(
                employee_id=employee.id,
                personal_email=f'{employee.id.hex[:5]}@example.com',
            )
            session.add(personal_info)
            financial_info = EmployeeFinancialInfoFactory.build(employee_id=employee.id)
            session.add(financial_info)

        session.commit()
        print('Seed completado exitosamente.')


if __name__ == '__main__':
    seed_employees(10)

import random

from decimal import Decimal

from common.database import engine
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlmodel import Session, SQLModel

# --- Importa tus modelos y tu engine aquí ---
# Asumo que tu archivo de modelos se llama 'employee_model.py' y tienes un 'database.py'
from models.employee_model import (
    Employee,
    EmployeeFinancialInfo,
    EmployeePersonalInfo,
    EmployeeStatus,
)


class EmployeeFactory(ModelFactory[Employee]):  # type: ignore[misc]
    __model__ = Employee

    # Forzar que el estado sea uno válido del Enum
    status = Use(lambda: random.choice(list(EmployeeStatus)))


class EmployeePersonalInfoFactory(ModelFactory[EmployeePersonalInfo]):  # type: ignore[misc]
    __model__ = EmployeePersonalInfo

    # Personalizamos campos para que parezcan reales
    personal_email = Use(ModelFactory.__faker__.email)
    first_name = Use(ModelFactory.__faker__.first_name)
    last_name = Use(ModelFactory.__faker__.last_name)
    city = Use(ModelFactory.__faker__.city)
    address = Use(ModelFactory.__faker__.address)

    # Excluimos employee_id de la generación automática aleatoria
    # porque se lo pasaremos manualmente
    __set_relationships__ = True


class EmployeeFinancialInfoFactory(ModelFactory[EmployeeFinancialInfo]):  # type: ignore[misc]
    __model__ = EmployeeFinancialInfo

    # Generar salarios realistas (ej. entre 2000 y 8000)
    salary_amount = Use(lambda: Decimal(random.randint(2000, 8000)))
    company_cost_amount = Use(lambda: Decimal(random.randint(2500, 9000)))


# ------------------------------------------------------------------
# 2. Función Orquestadora
# ------------------------------------------------------------------


def seed_employees(n: int = 10) -> None:
    SQLModel.metadata.create_all(engine)  # Asegura que las tablas existan

    with Session(engine) as session:
        print(f'🌱 Iniciando seed de {n} empleados completos...')

        for _ in range(n):
            # A) Crear el Empleado Base
            employee = EmployeeFactory.build()
            # Limpiamos IDs generados por factory para que la DB los asigne (si es auto-increment)
            # o dejamos que factory genere el UUID si tu modelo lo requiere.
            # En tu modelo el ID es UUID con default=None, Polyfactory generará uno.

            session.add(employee)
            # Hacemos flush para asegurar que 'employee' ya tiene un ID disponible en la sesión
            # (aunque con UUID generado por Python ya lo tenemos, pero es buena práctica)
            session.flush()

            # B) Crear Información Personal vinculada
            personal_info = EmployeePersonalInfoFactory.build(
                employee_id=employee.id,
                personal_email=f'{employee.id.hex[:5]}@example.com',  # Evitar duplicados únicos
            )
            session.add(personal_info)

            # C) Crear Información Financiera vinculada
            financial_info = EmployeeFinancialInfoFactory.build(employee_id=employee.id)
            session.add(financial_info)

        session.commit()
        print('Seed completado exitosamente.')


if __name__ == '__main__':
    seed_employees(10)

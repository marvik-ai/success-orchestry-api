import uuid
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Any, Optional, Self

from pydantic import model_validator
from sqlalchemy import DECIMAL, Column, String
from sqlmodel import Field, Relationship, SQLModel


class EmployeeStatus(str, PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class EmployeeBase(SQLModel):
    employee_code: str
    status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE)
    # current_position_id: uuid.UUID | None = Field(foreign_key='positions.id')


class EmployeePersonalInfoBase(SQLModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    document_number: str | None = Field(default=None, max_length=20)
    tax_id: str | None = Field(default=None, max_length=50)
    gender: str | None = Field(default=None, max_length=20)
    education_level: str | None = Field(default=None, max_length=50)
    # updatable profile
    personal_email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    phone: str | None = Field(default=None, max_length=50)
    photo: str | None = Field(
        default=None, max_length=100, description='URL o key de storage (S3/GCS)'
    )
    nickname: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=50)
    country_id: uuid.UUID | None = Field(default=None)
    address: str | None = Field(default=None, max_length=100)


class EmployeeFinancialInfoBase(SQLModel):
    salary_amount: Decimal = Field(default=0, sa_column=Column[Any](DECIMAL, nullable=False))
    salary_currency_id: uuid.UUID = Field(nullable=False)

    company_cost_amount: Decimal = Field(default=0, sa_column=Column(DECIMAL, nullable=False))

    effective_from: date = Field(nullable=False)
    effective_to: date | None = Field(default=None, description='NULL = registro actual')


class EmployeeCreate(EmployeeBase, EmployeePersonalInfoBase):
    # Nothing to add. Inherits name, country_id, etc.
    # Without an 'id', the user cannot send the failing "id: 0".
    pass


class EmployeeUpdate(EmployeeBase, EmployeePersonalInfoBase):
    employee_id: uuid.UUID


class EmployeeFinancialCreate(EmployeeFinancialInfoBase):
    pass


class EmployeePublicResponse(EmployeeBase, EmployeePersonalInfoBase):
    employee_id: uuid.UUID


class EmployeeFullResponse(EmployeePublicResponse, EmployeeFinancialInfoBase):
    pass


class Employee(EmployeeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    notes: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={'onupdate': lambda: datetime.now(UTC)},
    )
    deleted_at: datetime | None = Field(default=None)
    personal_info: Optional['EmployeePersonalInfo'] = Relationship(
        back_populates='employee', sa_relationship_kwargs={'uselist': False}
    )
    financial_info: Optional['EmployeeFinancialInfo'] = Relationship(
        back_populates='employee', sa_relationship_kwargs={'uselist': False}
    )


class EmployeePersonalInfo(EmployeePersonalInfoBase, table=True):
    __tablename__ = 'employees_personal_info'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key='employee.id', unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={'onupdate': lambda: datetime.now(UTC)},
    )
    deleted_at: datetime | None = Field(default=None)
    # inverse relationship
    employee: Employee | None = Relationship(back_populates='personal_info')


class EmployeeFinancialInfo(EmployeeFinancialInfoBase, table=True):
    __tablename__ = 'employee_financial_info'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key='employee.id', nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # inverse relationship
    employee: Employee | None = Relationship(back_populates='financial_info')

    @model_validator(mode='after')
    def validate_financial_logic(self) -> Self:
        # Regla: El sueldo no puede ser negativo
        if self.salary_amount < Decimal('0'):
            raise ValueError('El salario no puede ser negativo')

        # Regla: El costo de empresa no puede ser menor al salario bruto
        if self.company_cost_amount < self.salary_amount:
            raise ValueError('El costo de empresa no puede ser inferior al salario base')

        # Regla: Consistencia de fechas
        if self.effective_to and self.effective_to < self.effective_from:
            raise ValueError('La fecha de fin no puede ser anterior a la de inicio')

        return self

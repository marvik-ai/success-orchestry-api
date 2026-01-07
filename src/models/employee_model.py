import re
import uuid

from datetime import UTC, date, datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Any, Optional

from pydantic import field_validator, model_validator
from sqlalchemy import DECIMAL, Column, String
from sqlmodel import Field, Relationship, SQLModel


class EmployeeStatus(str, PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class EmployeeBase(SQLModel):
    employee_code: str
    status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE)
    # current_position_id: uuid.UUID | None = Field(foreign_key='positions.id')

    # Validators
    @field_validator('employee_code')
    @classmethod
    def validate_employee_code_format(cls, v: str) -> str:
        v = v.upper().strip()
        pattern = r'^[A-Z]{3}-\d{3}$'
        if not re.match(pattern, v):
            raise ValueError(
                'El código del empleado debe seguir el formato AAA-000 (3 letras, guión, 3 números)'
            )
        return v


class EmployeePersonalInfoBase(SQLModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    document_number: str | None = Field(default=None, max_length=20)
    tax_id: str | None = Field(default=None, max_length=50)
    gender: str | None = Field(default=None, max_length=20)
    education_level: str | None = Field(default=None, max_length=50)
    personal_email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    phone: str | None = Field(default=None, max_length=50)
    photo: str | None = Field(
        default=None, max_length=100, description='URL o key de storage (S3/GCS)'
    )
    nickname: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=50)
    country_id: uuid.UUID | None = Field(default=None)
    address: str | None = Field(default=None, max_length=100)

    # Validators
    @field_validator('first_name', 'last_name', 'city')
    @classmethod
    def title_case(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().title()

    @field_validator('personal_email')
    @classmethod
    def lower_case_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator('document_number', 'tax_id')
    @classmethod
    def clean_document(cls, v: str | None) -> str | None:
        if v:
            # Elimina espacios, guiones y puntos
            return v.replace('-', '').replace('.', '').replace(' ', '').upper()
        return v


class EmployeeFinancialInfoBase(SQLModel):
    salary_amount: Decimal = Field(default=0, sa_column=Column[Any](DECIMAL, nullable=False))
    salary_currency_id: uuid.UUID = Field(nullable=False)

    company_cost_amount: Decimal = Field(default=0, sa_column=Column(DECIMAL, nullable=False))

    effective_from: date = Field(nullable=False)
    effective_to: date | None = Field(default=None, description='NULL = registro actual')

    # Validators
    @field_validator('salary_amount', 'company_cost_amount')
    @classmethod
    def must_be_positive(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError('El monto no puede ser negativo')
        return v

    @model_validator(mode='after')
    def check_dates(self) -> 'EmployeeFinancialInfoBase':
        if self.effective_to is not None and self.effective_to < self.effective_from:
            raise ValueError(
                'La fecha de fin (effective_to) no puede ser anterior al inicio (effective_from)'
            )
        return self


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
    # The table class inherits base fields and adds DB-specific fields
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

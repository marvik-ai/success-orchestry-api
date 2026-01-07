import re
import uuid
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Optional, Self

from pydantic import field_validator, model_validator
from sqlalchemy import DECIMAL, Column, String
from sqlmodel import Field, Relationship, SQLModel


class EmployeeStatus(str, PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class EmployeeBase(SQLModel):
    employee_code: str
    status: str

    @field_validator('employee_code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('El código debe ser alfanumérico')
        return v.upper().strip()


class EmployeeCreate(EmployeeBase):
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

    @model_validator(mode='after')
    def validate_business_state(self) -> Self:
        if self.deleted_at and self.status == EmployeeStatus.ACTIVE:
            raise ValueError('Cierre el estado del empleado antes de eliminarlo')

        if self.status == EmployeeStatus.INACTIVE and not self.notes:
            raise ValueError("Debe registrar una razón en 'notes' para la desactivación")

        return self


class EmployeePersonalInfo(SQLModel, table=True):
    __tablename__ = 'employees_personal_info'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key='employee.id', unique=True)
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

    employee: Employee | None = Relationship(back_populates='personal_info')

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v: str) -> str:
        v = v.strip()
        # Regex para letras latinas, tildes y espacios internos.
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', v):
            raise ValueError('Solo se permiten letras y tildes (sin símbolos)')
        return v

    @field_validator('document_number', 'phone')
    @classmethod
    def validate_only_numbers(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v.isdigit():
            raise ValueError('Este campo debe contener solo números')
        return v

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v.isalnum():
            raise ValueError('El apodo solo puede contener letras y números')
        return v

    @field_validator('personal_email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Formato de correo electrónico inválido')
        return v


class EmployeeFinancialInfo(SQLModel, table=True):
    __tablename__ = 'employee_financial_info'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key='employee.id', nullable=False)

    salary_amount: Decimal = Field(default=0, sa_column=Column(DECIMAL, nullable=False))
    salary_currency_id: uuid.UUID = Field(nullable=False)
    company_cost_amount: Decimal = Field(default=0, sa_column=Column(DECIMAL, nullable=False))

    effective_from: date = Field(nullable=False)
    effective_to: date | None = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

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

import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, List, Optional
from enum import Enum as PyEnum

from sqlmodel import Field, SQLModel, Relationship, create_engine
from sqlalchemy import Column, String, DECIMAL, text


class EmployeeStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class EmployeeBase(SQLModel):
    employee_code: str
    status: str
    current_position_id: Optional[uuid.UUID] = Field(foreign_key="positions.id")


class EmployeeCreate(EmployeeBase):
    # Nothing to add. Inherits name, country_id, etc.
    # Without an 'id', the user cannot send the failing "id: 0".
    pass

class Employee(EmployeeBase, table=True):
    # The table class inherits base fields and adds DB-specific fields
    id: Optional[int] = Field(default=None, primary_key=True)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})
    deleted_at: Optional[datetime] = Field(default=None)
    personal_info: Optional["EmployeePersonalInfo"] = Relationship(back_populates="employee", sa_relationship_kwargs={"uselist": False})
    financial_info: Optional["EmployeeFinancialInfo"] = Relationship(back_populates="employee", sa_relationship_kwargs={"uselist": False})

class EmployeePersonalInfo(SQLModel, table=True):
    __tablename__ = "employees_personal_info"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Relación 1 a 1 con Employee
    employee_id: uuid.UUID = Field(foreign_key="employees.id", unique=True)
    
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    document_number: Optional[str] = Field(default=None, max_length=20)
    tax_id: Optional[str] = Field(default=None, max_length=50)
    
    gender: Optional[str] = Field(default=None, max_length=20)
    education_level: Optional[str] = Field(default=None, max_length=50)

    # Perfil editable
    personal_email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    phone: Optional[str] = Field(default=None, max_length=50)
    photo: Optional[str] = Field(default=None, max_length=100, description="URL o key de storage (S3/GCS)")
    nickname: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=50)
    country_id: Optional[uuid.UUID] = Field(default=None)
    address: Optional[str] = Field(default=None, max_length=100)

    # Relación inversa
    employee: Optional[Employee] = Relationship(back_populates="personal_info")


class EmployeeFinancialInfo(SQLModel, table=True):
    """
    Historial salarial.
    ACCESO RESTRINGIDO: Solo SUPER_ADMIN, ADMIN, HR.
    """
    __tablename__ = "employee_financial_info"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key="employees.id", nullable=False)

    salary_amount: Decimal = Field(default=0, sa_column=Column[Any](DECIMAL, nullable=False))
    salary_currency_id: uuid.UUID = Field(nullable=False)
    
    company_cost_amount: Decimal = Field(default=0, sa_column=Column(DECIMAL, nullable=False))

    effective_from: date = Field(nullable=False)
    effective_to: Optional[date] = Field(default=None, description="NULL = registro actual")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relación inversa
    employee: Optional[Employee] = Relationship(back_populates="financial_info")
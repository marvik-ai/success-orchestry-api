from datetime import UTC, datetime
from enum import Enum as PyEnum

from sqlmodel import Field, SQLModel


class EmployeeStatus(str, PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class EmployeeBase(SQLModel):
    employee_code: str
    status: str
    # current_position_id: uuid.UUID | None = Field(foreign_key='positions.id')


class EmployeeCreate(EmployeeBase):
    # Nothing to add. Inherits name, country_id, etc.
    # Without an 'id', the user cannot send the failing "id: 0".
    pass


class Employee(EmployeeBase, table=True):
    # The table class inherits base fields and adds DB-specific fields
    id: int | None = Field(default=None, primary_key=True)
    notes: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={'onupdate': lambda: datetime.now(UTC)},
    )
    deleted_at: datetime | None = Field(default=None)
    # personal_info: Optional['EmployeePersonalInfo'] = Relationship(
    #     back_populates='employee', sa_relationship_kwargs={'uselist': False}
    # )
    # financial_info: Optional['EmployeeFinancialInfo'] = Relationship(
    #    back_populates='employee', sa_relationship_kwargs={'uselist': False}
    # )

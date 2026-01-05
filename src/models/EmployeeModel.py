from typing import Optional
from sqlmodel import Field, SQLModel

class EmployeeBase(SQLModel):
    # These are the fields the user sends AND you see when querying
    name: str

class EmployeeCreate(EmployeeBase):
    # Nothing to add. Inherits name, country_id, etc.
    # Without an 'id', the user cannot send the failing "id: 0".
    pass

class Employee(EmployeeBase, table=True):
    # The table class inherits base fields and adds DB-specific fields
    id: Optional[int] = Field(default=None, primary_key=True)

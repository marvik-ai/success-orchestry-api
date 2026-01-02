from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

# This avoids circular import errors for type hinting
if TYPE_CHECKING:
    from app.Models.UserModel import User
    from app.Models.SeniorityModel import Seniority
    from app.Models.CountryModel import Country
    from app.Models.RoleModel import Role

class EmployeeBase(SQLModel):
    # These are the fields the user sends AND you see when querying
    name: str
    country_id: int = Field(foreign_key="country.id")
    seniority_id: int = Field(foreign_key="seniority.id")
    role_id: int = Field(foreign_key="role.id")

class EmployeeCreate(EmployeeBase):
    # Nothing to add. Inherits name, country_id, etc.
    # Without an 'id', the user cannot send the failing "id: 0".
    pass

class Employee(EmployeeBase, table=True):
    # The table class inherits base fields and adds DB-specific fields
    id: Optional[int] = Field(default=None, primary_key=True)

    # RELATIONSHIPS (objects) live ONLY here.
    # They do not appear in creation JSON; they are for joins in queries.
    user: Optional["User"] = Relationship(back_populates="employee")
    country: "Country" = Relationship()
    seniority: "Seniority" = Relationship()
    role: "Role" = Relationship()

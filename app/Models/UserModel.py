from re import S
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
from app.Models.EmployeeModel import Employee

class UserRole(str,Enum):
    admin = "admin"
    user = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str 
    role: UserRole = Field(default=UserRole.user)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Optional["Employee"] = Relationship(back_populates="user")
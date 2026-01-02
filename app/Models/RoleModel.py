from sqlmodel import SQLModel, Field
from typing import Optional

class RoleBase(SQLModel):
    role_name : str = Field(index=True)

class RoleCreate(RoleBase):
    pass

class Role(RoleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


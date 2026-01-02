from sqlmodel import SQLModel, Field
from typing import Optional

class SeniorityBase(SQLModel):
    seniority_name: str = Field(index=True)

class SeniorityCreate(SeniorityBase):
    pass

class Seniority(SeniorityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    


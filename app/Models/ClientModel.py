from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class ClientStatus(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: str = Field(index=True)
    client_code: str = Field(unique=True, index=True) # Unique identifier
    industry: str
    country: str
    company_size: str
    msa: Optional[str] = None # MSA URL
    first_project_date: Optional[date]  # Use date for better DB handling
    status: ClientStatus = Field(default=ClientStatus.activo)

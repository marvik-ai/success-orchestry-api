from sqlmodel import SQLModel, Field
from typing import Optional

from sqlmodel import SQLModel, Field
from typing import Optional

# 1. Base class with common fields
class CountryBase(SQLModel):
    country_name: str

# 2. Class for CREATE (no ID)
class CountryCreate(CountryBase):
    pass  # No ID here; Swagger will not request it

# 3. Database class (has ID and is a table)
class Country(CountryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


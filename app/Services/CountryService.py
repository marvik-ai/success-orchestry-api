from app.Models.CountryModel import Country, CountryCreate
from app.Database.Repositories.CountryRepository import CountryRepositoryClass
from typing import List

class CountryService:
    def __init__(self, country_repo: CountryRepositoryClass) -> None:
        self.country_repo = country_repo

    def get_all(self) -> List[Country]:
        return self.country_repo.get()

    def add(self, country: CountryCreate) -> Country:        
        return self.country_repo.add(country)
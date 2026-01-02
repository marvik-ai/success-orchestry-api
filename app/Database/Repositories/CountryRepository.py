from sqlmodel import Session, select
from app.Models.CountryModel import Country, CountryCreate

class CountryRepositoryClass:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self):
        return self.session.exec(select(Country)).all()

    def add(self, country : CountryCreate):
        db_client = Country.model_validate(country)
        self.session.add(db_client)
        self.session.commit()
        self.session.refresh(db_client)
        return db_client
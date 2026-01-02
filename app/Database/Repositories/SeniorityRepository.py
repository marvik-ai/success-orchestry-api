from app.Models.SeniorityModel import Seniority , SeniorityCreate
from sqlmodel import Session, select

class SeniorityRepositoryClass:
    def __init__(self, session : Session) -> None:
        self.session = session

    def get(self):
        return self.session.exec(select(Seniority)).all()

    def add(self, seniority : SeniorityCreate):
        db_client = Seniority.model_validate(seniority)
        self.session.add(db_client)
        self.session.commit()
        self.session.refresh(db_client)
        return db_client
from sqlalchemy import text
from sqlmodel import Session


class HealthService:
    def __init__(self, session: Session):
        self.session = session

    def check(self) -> dict:
        self.session.exec(text("SELECT 1"))
        return {"status": "ok"}

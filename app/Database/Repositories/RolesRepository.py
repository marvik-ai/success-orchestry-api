from app.Models.RoleModel import Role, RoleCreate
from sqlmodel import Session, select

class RoleRepositoryClass:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self):
        return self.session.exec(select(Role)).all()

    def add(self, role : RoleCreate):
        db_model = Role.model_validate(role)
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model
        

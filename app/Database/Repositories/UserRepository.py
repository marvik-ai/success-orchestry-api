from sqlmodel import Session, select
from app.Models.UserModel import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def getUserByEmail(self, email:str):
        user = self.session.exec(select (User).where(User.email == email)).first()
        return user
from app.Models.EmployeeModel import Employee
from app.Models.UserModel import User
from app.Database.Repositories.UserRepository import UserRepository
from app.Database.Repositories.EmployeeRepository import EmployeeRepositoryClass
from app.security import verify_password, create_token, validate_token, get_password_hash

class AuthService:
    def __init__(self, user_repo: UserRepository, emp_repo: EmployeeRepositoryClass):
        self.user_repo = user_repo
        self.emp_repo = emp_repo

    def register_user(self, user_data: dict):
        plain_password = user_data.get("password")
        print(f"DEBUG: Password type: {type(plain_password)} Length: {len(str(plain_password))}")
        hashed_pw = get_password_hash(plain_password)

        new_employee = Employee(
            name=user_data.get("name"),
            email=user_data.get("email")
        )
        created_employee = self.emp_repo.create_employee(new_employee)
       
        new_user = User(
            name=user_data.get("name"),
            email=user_data.get("email"),
            password=hashed_pw,
            role=user_data.get("role", "user"),
            employee_id=created_employee.id
        )
        
        return self.user_repo.create_user(new_user)
    
    def login(self, email:str, password:str):
        user = self.user_repo.getUserByEmail(email)
        if not user:
            return None
        
        is_valid = verify_password(password, user.password)
        
        if not is_valid:
            return None
            
        token = create_token(subject=user.email)
        
        return {
            "access_token": token, 
            "token_type": "bearer"
        }

    def get_user_from_token(self, token: str):
        # 1. Decode logic (Security layer)
        email = validate_token(token)
        
        # 2. Persistence logic (Repository layer)
        user = self.user_repo.getUserByEmail(email)
        
        return user

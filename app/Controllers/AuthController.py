from fastapi import APIRouter, Depends, HTTPException, status
from app.Services.AuthService import AuthService
from app.Models.UserModel import User
from app.Models.LoginModel import Login
from app.dependencies import get_auth_services, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies = [Depends(get_current_user)])

@router.post("/register")
def register(user_in: User, service: AuthService = Depends(get_auth_services)):
    return service.register_user(user_in.model_dump())

@router.post("/login")
def login(login_in: Login, service: AuthService = Depends(get_auth_services)):
    auth_result = service.login(login_in.email, login_in.password)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    return auth_result

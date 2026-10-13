from fastapi import APIRouter, Depends

from app.dto.user_dto import CredentialsRequest, TokenResponse, UserResponse
from app.entity.user import User
from app.service.auth_service import AuthService
from app.util.dependencies import get_auth_service, get_current_user

router = APIRouter(tags=["auth"])


@router.post("/auth/register", response_model=UserResponse, status_code=201)
def register(body: CredentialsRequest, service: AuthService = Depends(get_auth_service)):
    return UserResponse.model_validate(service.register(body))


@router.post("/auth/login", response_model=TokenResponse)
def login(body: CredentialsRequest, service: AuthService = Depends(get_auth_service)):
    return TokenResponse(access_token=service.login(body))


@router.get("/users/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)

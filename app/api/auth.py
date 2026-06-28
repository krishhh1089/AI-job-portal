from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.register(
            db,
            user_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        login_data = LoginRequest(
            email=form_data.username,
            password=form_data.password
        )

        access_token = AuthService.login(
            db,
            login_data
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
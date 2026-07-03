from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User, UserRole

from app.schemas.user import (
    UserResponse,
    UpdateUserRequest
)

from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =====================================
# GET MY PROFILE
# =====================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# =====================================
# UPDATE MY PROFILE
# =====================================

@router.patch(
    "/me",
    response_model=UserResponse
)
def update_my_profile(
    user_data: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
        return UserService.update_user(
            db=db,
            user=current_user,
            user_data=user_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =====================================
# DELETE MY ACCOUNT
# =====================================

@router.delete("/me")
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    UserService.delete_user(
        db=db,
        user=current_user
    )

    return {
        "message": "Account processed successfully."
    }


# =====================================
# GET ALL USERS (ADMIN)
# =====================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all users."
        )

    return UserService.get_all_users(db)


# =====================================
# GET USER BY ID (ADMIN)
# =====================================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view users."
        )

    user = UserService.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return user


# =====================================
# ACTIVATE USER (ADMIN)
# =====================================

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse
)
def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can activate users."
        )

    user = UserService.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return UserService.activate_user(
        db,
        user
    )


# =====================================
# DEACTIVATE USER (ADMIN)
# =====================================

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse
)
def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can deactivate users."
        )

    user = UserService.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    if current_user.user_id == user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot deactivate their own account."
        )

    return UserService.deactivate_user(
        db,
        user
    )
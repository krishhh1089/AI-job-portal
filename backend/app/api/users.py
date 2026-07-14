# app/routers/user_router.py

# app/routers/user_router.py

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User, UserRole

from app.schemas.user import (
    UserResponse,
    UserListResponse,
    UpdateUserRequest
)

from app.services.user_service import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=UserListResponse
)
def get_all_users(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100
    ),

    role: UserRole | None = Query(
        default=None
    ),

    is_active: bool | None = Query(
        default=None
    ),

    is_verified: bool | None = Query(
        default=None
    ),

    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|email|last_login)$"
    ),

    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    cursor: str | None = Query(
        default=None
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):
    return user_service.get_all_users(
        db=db,
        current_user=current_user,
        limit=limit,
        cursor=cursor,
        search=search,
        role=role,
        is_active=is_active,
        is_verified=is_verified,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.patch(
    "/me",
    response_model=UserResponse
)
def update_my_profile(
    user_data: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.update_user(
        db=db,
        user=current_user,
        user_data=user_data
    )


@router.delete("/me")
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_service.delete_user(
        db=db,
        user=current_user
    )

    return {
        "message": "Account processed successfully."
    }


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_all_users(
        db=db,
        current_user=current_user
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.get_user_by_id(
        db=db,
        user_id=user_id,
        current_user=current_user
    )


@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse
)
def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.activate_user(
        db=db,
        user_id=user_id,
        current_user=current_user
    )


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse
)
def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.deactivate_user(
        db=db,
        user_id=user_id,
        current_user=current_user
    )
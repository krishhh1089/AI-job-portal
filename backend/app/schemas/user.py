# app/schemas/user.py

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole
from app.schemas.base import TimestampResponse


# =====================================
# USER RESPONSE
# =====================================

class UserResponse(TimestampResponse):
    user_id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


# =====================================
# USER UPDATE
# normal user can update only email
# =====================================

class UpdateUserRequest(BaseModel):
    email: EmailStr | None = None


# =====================================
# ADMIN USER UPDATE
# admin can activate/deactivate user
# =====================================

class AdminUpdateUserRequest(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    role: UserRole | None = None


# =====================================
# USER LIST RESPONSE
# =====================================

class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
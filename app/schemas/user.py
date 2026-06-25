from uuid import UUID
from datetime import datetime
from pydantic import Field

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    profile_picture: str | None = None


class UserRead(UserBase):
    user_id: UUID
    role: str
    profile_picture: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
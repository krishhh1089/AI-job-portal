from pydantic import BaseModel, EmailStr

from app.models.user import UserRole

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class RegisterRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    role: UserRole

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value
# =====================================
# LOGIN REQUEST
# =====================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =====================================
# TOKEN RESPONSE
# =====================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
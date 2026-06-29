from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


# =====================================
# REGISTER REQUEST
# =====================================

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.JOBSEEKER


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
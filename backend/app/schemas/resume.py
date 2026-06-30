# app/schemas/resume.py

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import TimestampResponse


# =====================================
# RESUME UPDATE
# =====================================

class UpdateResumeRequest(BaseModel):
    file_name: str | None = None
    is_default: bool | None = None


# =====================================
# RESUME RESPONSE
# =====================================

class ResumeResponse(TimestampResponse):
    resume_id: UUID
    user_id: UUID
    file_path: str
    file_name: str | None
    is_default: bool

    class Config:
        from_attributes = True
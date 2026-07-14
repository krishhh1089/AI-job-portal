from uuid import UUID

from pydantic import BaseModel

from app.models.application import ApplicationStatus
from app.schemas.base import TimestampResponse


class CreateApplicationRequest(BaseModel):
    job_id: UUID
    resume_id: UUID
    cover_letter: str | None = None


class UpdateApplicationStatusRequest(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(TimestampResponse):
    application_id: UUID
    job_id: UUID
    user_id: UUID
    resume_id: UUID
    cover_letter: str | None
    status: ApplicationStatus

    class Config:
        from_attributes = True

class ApplicationListResponse(BaseModel):
    items: list[ApplicationResponse]
    next_cursor: str | None = None
    has_next: bool
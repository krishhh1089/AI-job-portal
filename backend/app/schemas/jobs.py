from typing import List
from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.jobs import (
    JobType,
    JobStatus
)
from app.schemas.base import TimestampResponse


# ==========================================================
# CREATE JOB
# ==========================================================

class CreateJobRequest(BaseModel):

    title: str

    description: str

    responsibilities: str | None = None

    requirements: str | None = None

    job_type: JobType

    location: str | None = None

    is_remote: bool = False

    salary_min: int | None = None

    salary_max: int | None = None

    currency: str = "INR"

    experience_min: int | None = None

    experience_max: int | None = None

    application_deadline: date | None = None


    skill_ids: list[UUID] = Field(default_factory=list)


# ==========================================================
# UPDATE JOB
# ==========================================================

class UpdateJobRequest(BaseModel):

    title: str | None = None

    description: str | None = None

    responsibilities: str | None = None

    requirements: str | None = None

    job_type: JobType | None = None

    status: JobStatus | None = None

    location: str | None = None

    is_remote: bool | None = None

    salary_min: int | None = None

    salary_max: int | None = None

    currency: str | None = None

    experience_min: int | None = None

    experience_max: int | None = None

    application_deadline: date | None = None

    skill_ids: list[UUID] = Field(default_factory=list)


# ==========================================================
# JOB RESPONSE
# ==========================================================

class JobResponse(TimestampResponse):

    job_id: UUID

    company_id: UUID

    posted_by: UUID

    title: str

    description: str

    responsibilities: str | None

    requirements: str | None

    job_type: JobType

    status: JobStatus

    location: str | None

    is_remote: bool

    salary_min: int | None

    salary_max: int | None

    currency: str | None

    experience_min: int | None

    experience_max: int | None

    application_deadline: date | None

    class Config:
        from_attributes = True

      



class CursorJobListResponse(BaseModel):
    limit: int
    next_cursor: str | None
    jobs: List[JobResponse]
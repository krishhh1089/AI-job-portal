import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    Date,
    ForeignKey,
    Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


# ==========================================================
# JOB TYPE ENUM
# ==========================================================

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    REMOTE = "remote"


# ==========================================================
# JOB STATUS ENUM
# ==========================================================

class JobStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"


# ==========================================================
# JOB MODEL
# ==========================================================

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    # ------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------

    job_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # ------------------------------------------------------
    # COMPANY / RECRUITER
    # ------------------------------------------------------

    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "companies.company_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    posted_by = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    # ------------------------------------------------------
    # JOB DETAILS
    # ------------------------------------------------------

    title = Column(
        String(255),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=False
    )

    responsibilities = Column(
        Text,
        nullable=True
    )

    requirements = Column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # JOB TYPE / STATUS
    # ------------------------------------------------------

    job_type = Column(
        SAEnum(
            JobType,
            name="job_type"
        ),
        nullable=False
    )

    status = Column(
        SAEnum(
            JobStatus,
            name="job_status"
        ),
        nullable=False,
        default=JobStatus.ACTIVE
    )

    # ------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------

    location = Column(
        String(255),
        nullable=True,
        index=True
    )

    is_remote = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # ------------------------------------------------------
    # SALARY
    # ------------------------------------------------------

    salary_min = Column(
        Integer,
        nullable=True
    )

    salary_max = Column(
        Integer,
        nullable=True
    )

    currency = Column(
        String(10),
        nullable=True,
        default="INR"
    )

    # ------------------------------------------------------
    # EXPERIENCE
    # ------------------------------------------------------

    experience_min = Column(
        Integer,
        nullable=True
    )

    experience_max = Column(
        Integer,
        nullable=True
    )

    # ------------------------------------------------------
    # DEADLINE
    # ------------------------------------------------------

    application_deadline = Column(
        Date,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------

    company = relationship(
        "Company",
        back_populates="jobs"
    )

    recruiter = relationship(
        "User",
        back_populates="jobs"
    )

    job_skills = relationship(
        "JobSkill",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    # applications will be added later
    # job_skills will be added later

    # ------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------

    def __repr__(self):
        return (
            f"<Job("
            f"job_id={self.job_id}, "
            f"title='{self.title}', "
            f"status='{self.status.value}'"
            f")>"
        )
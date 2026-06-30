import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    Text,
    ForeignKey,
    Enum as SAEnum,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    REVIEWING = "Reviewing"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"
    HIRED = "Hired"
    WITHDRAWN = "Withdrawn"


class Application(Base, TimestampMixin):
    __tablename__ = "applications"

    application_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "jobs.job_id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.user_id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    resume_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "resumes.resume_id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    cover_letter = Column(
        Text,
        nullable=True
    )

    status = Column(
        SAEnum(
            ApplicationStatus,
            name="application_status"
        ),
        nullable=False,
        default=ApplicationStatus.APPLIED
    )

    job = relationship(
        "Job",
        back_populates="applications"
    )

    user = relationship(
        "User",
        back_populates="applications"
    )

    resume = relationship(
        "Resume",
        back_populates="applications"
    )

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "user_id",
            name="unique_user_job_application"
        ),
    )
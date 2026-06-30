# app/models/user.py

import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


# ==========================================================
# USER ROLE ENUM
# ==========================================================

class UserRole(str, Enum):
    JOBSEEKER = "jobseeker"
    RECRUITER = "recruiter"
    ADMIN = "admin"


# ==========================================================
# USER MODEL
# ==========================================================

class User(Base, TimestampMixin):
    __tablename__ = "users"

    # ------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # ------------------------------------------------------
    # AUTHENTICATION
    # ------------------------------------------------------

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        Text,
        nullable=False
    )

    role = Column(
        SAEnum(
            UserRole,
            name="user_role"
        ),
        nullable=False,
        default=UserRole.JOBSEEKER
    )

    # ------------------------------------------------------
    # ACCOUNT STATUS
    # ------------------------------------------------------

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    is_verified = Column(
        Boolean,
        nullable=False,
        default=False
    )

    last_login = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # ------------------------------------------------------
    # EMAIL VERIFICATION
    # ------------------------------------------------------

    email_verification_token = Column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # PASSWORD RESET
    # ------------------------------------------------------

    password_reset_token = Column(
        Text,
        nullable=True
    )

    password_reset_expires = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # ------------------------------------------------------
    # RECRUITER COMPANY
    # ------------------------------------------------------

    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "companies.company_id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------

    applications = relationship(
    "Application",
    back_populates="user"
    )

    resumes = relationship(
    "Resume",
    back_populates="user",
    cascade="all, delete-orphan"
    )

    company = relationship(
    "Company",
    back_populates="recruiters"
    )

    jobs = relationship(
    "Job",
    back_populates="recruiter"
    )
    
    # ------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------

    def __repr__(self):
        return (
            f"<User("
            f"user_id={self.user_id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}'"
            f")>"
        )
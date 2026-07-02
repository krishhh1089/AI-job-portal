import uuid
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    String,
    Text,
    Integer,
    Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


# ==========================================================
# INDUSTRY ENUM
# ==========================================================

class Industry(str, Enum):
    SOFTWARE = "Software"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    ECOMMERCE = "E-Commerce"
    MANUFACTURING = "Manufacturing"
    OTHER = "Other"


# ==========================================================
# COMPANY SIZE ENUM
# ==========================================================

class CompanySize(str, Enum):
    ONE_TO_TEN = "1-10"
    ELEVEN_TO_FIFTY = "11-50"
    FIFTY_ONE_TO_TWO_HUNDRED = "51-200"
    TWO_HUNDRED_ONE_TO_FIVE_HUNDRED = "201-500"
    FIVE_HUNDRED_PLUS = "500+"


# ==========================================================
# COMPANY MODEL
# ==========================================================

class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    # ------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------

    company_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # ------------------------------------------------------
    # BASIC INFORMATION
    # ------------------------------------------------------

    name = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    website = Column(
        String(255),
        nullable=True
    )

    industry = Column(
        SAEnum(
            Industry,
            name="industry"
        ),
        nullable=False
    )
    
    is_active = Column(
        Boolean,
        nullable=False,
        default=True
        )

    company_size = Column(
        SAEnum(
            CompanySize,
            name="company_size"
        ),
        nullable=False
    )

    location = Column(
        String(255),
        nullable=True
    )

    founded_year = Column(
        Integer,
        nullable=True
    )

    logo_url = Column(
        Text,
        nullable=True
    )

    # ------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------

    recruiters = relationship(
        "User",
        back_populates="company"
    )

    jobs = relationship(
        "Job",
        back_populates="company"
    )

    # ------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------

    def __repr__(self):
        return (
            f"<Company("
            f"company_id={self.company_id}, "
            f"name='{self.name}'"
            f")>"
        )
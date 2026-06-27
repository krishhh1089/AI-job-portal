import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


# ==========================================================
# SKILL CATEGORY ENUM
# ==========================================================

class SkillCategory(str, Enum):
    PROGRAMMING = "programming"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    DEVOPS = "devops"
    TOOL = "tool"
    SOFT_SKILL = "soft_skill"
    OTHER = "other"


# ==========================================================
# SKILL MODEL
# ==========================================================

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    # ------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------

    skill_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # ------------------------------------------------------
    # BASIC INFORMATION
    # ------------------------------------------------------

    name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    category = Column(
        SAEnum(
            SkillCategory,
            name="skill_category"
        ),
        nullable=False
    )

    # ------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------
    job_skills = relationship(
        "JobSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )
    # Will be added later

    # user_skills
    # job_skills

    # ------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------

    def __repr__(self):
        return (
            f"<Skill("
            f"skill_id={self.skill_id}, "
            f"name='{self.name}'"
            f")>"
        )
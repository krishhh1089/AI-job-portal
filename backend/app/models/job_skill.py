from sqlalchemy import (
    Column,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class JobSkill(Base):
    __tablename__ = "job_skills"

    # =====================================
    # COMPOSITE PRIMARY KEY
    # =====================================

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "jobs.job_id",
            ondelete="CASCADE"
        ),
        primary_key=True 
    )

    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "skills.skill_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    job = relationship(
        "Job",
        back_populates="job_skills"
    )

    skill = relationship(
        "Skill",
        back_populates="job_skills"
    )
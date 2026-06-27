from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.models.skill import SkillCategory


# ==========================================================
# CREATE SKILL
# ==========================================================

class CreateSkillRequest(BaseModel):

    name: str

    category: SkillCategory


# ==========================================================
# UPDATE SKILL
# ==========================================================

class UpdateSkillRequest(BaseModel):

    name: str | None = None

    category: SkillCategory | None = None


# ==========================================================
# SKILL RESPONSE
# ==========================================================

class SkillResponse(BaseModel):

    skill_id: UUID

    name: str

    category: SkillCategory

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True
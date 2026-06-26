from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.models.company import (
    Industry,
    CompanySize
)


# ==========================================================
# CREATE COMPANY
# ==========================================================

class CreateCompanyRequest(BaseModel):

    name: str

    description: str | None = None

    website: HttpUrl | None = None

    industry: Industry

    company_size: CompanySize

    location: str | None = None

    founded_year: int | None = None

    logo_url: HttpUrl | None = None


# ==========================================================
# UPDATE COMPANY
# ==========================================================

class UpdateCompanyRequest(BaseModel):

    name: str | None = None

    description: str | None = None

    website: HttpUrl | None = None

    industry: Industry | None = None

    company_size: CompanySize | None = None

    location: str | None = None

    founded_year: int | None = None

    logo_url: HttpUrl | None = None


# ==========================================================
# COMPANY RESPONSE
# ==========================================================

class CompanyResponse(BaseModel):

    company_id: UUID

    name: str

    description: str | None

    website: HttpUrl | None

    industry: Industry

    company_size: CompanySize

    location: str | None

    founded_year: int | None

    logo_url: HttpUrl | None

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

class JobType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    remote = "remote"

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    job_type: JobType
    description: str
    required_skills: list[str]
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None

class JobResponse(JobCreate):
    id: int
    posted_by: str
    created_at: datetime

    class Config:
        from_attributes = True   # lets Pydantic read SQLAlchemy objects

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "jobseeker"
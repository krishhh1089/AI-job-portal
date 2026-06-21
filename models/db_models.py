from sqlalchemy import Column, Integer, String, Text, ARRAY, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from database import Base
import enum

class JobTypeEnum(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    remote = "remote"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="jobseeker")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    job_type = Column(SAEnum(JobTypeEnum), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(ARRAY(String), default=[])
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    posted_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
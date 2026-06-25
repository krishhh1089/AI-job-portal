import uuid
from sqlalchemy import (
    Column, String, Text, Boolean, Integer,
    Date, ForeignKey, DateTime, Numeric,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from enum import Enum


# ──────────────────────────────────────────
# 1. USERS
# Core auth only — nothing else
# ──────────────────────────────────────────

class UserRole(str, Enum):
    JOBSEEKER = "jobseeker"
    RECRUITER = "recruiter"
    ADMIN = "admin"
    
class User(Base):
    __tablename__ = "users"

    user_id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email         = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum(UserRole),nullable=False,default=UserRole.JOBSEEKER)  # jobseeker | recruiter | admin
    is_verified   = Column(Boolean, default=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), server_default=func.now(),
                           onupdate=func.now())

    # relationships — one user owns all of these
    profile       = relationship("UserProfile",      back_populates="user", uselist=False)
    skills        = relationship("UserSkill",         back_populates="user")
    educations    = relationship("Education",         back_populates="user")
    experiences   = relationship("Experience",        back_populates="user")
    certifications= relationship("Certification",     back_populates="user")
    projects      = relationship("Project",           back_populates="user")
    languages     = relationship("UserLanguage",      back_populates="user")


# ──────────────────────────────────────────
# 2. USER PROFILES
# Everything personal — separate from auth
# ──────────────────────────────────────────

class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.user_id"),
                             unique=True, nullable=False)
    headline        = Column(String(255), nullable=True)   # "Final year CSE student | Python dev"
    bio             = Column(Text, nullable=True)
    phone           = Column(String(20), nullable=True)
    location        = Column(String(255), nullable=True)
    date_of_birth   = Column(Date, nullable=True)
    profile_picture = Column(Text, nullable=True)          # S3 URL

    # social links — stored here since they're fixed, known fields
    github      = Column(Text, nullable=True)
    linkedin    = Column(Text, nullable=True)
    portfolio   = Column(Text, nullable=True)
    leetcode    = Column(Text, nullable=True)
    hackerrank  = Column(Text, nullable=True)

    user = relationship("User", back_populates="profile")


# ──────────────────────────────────────────
# 3. SKILLS (global lookup table)
# Shared across users and jobs
# ──────────────────────────────────────────

class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=True)  # "Backend" | "ML" | "DevOps" | "Frontend"

    user_skills = relationship("UserSkill", back_populates="skill")


# ──────────────────────────────────────────
# 4. USER SKILLS
# Many-to-many: user ↔ skill
# ──────────────────────────────────────────

class UserSkill(Base):
    __tablename__ = "user_skills"
    __table_args__ = (UniqueConstraint("user_id", "skill_id"),)

    user_id            = Column(UUID(as_uuid=True), ForeignKey("users.user_id"),
                                primary_key=True)
    skill_id           = Column(Integer, ForeignKey("skills.skill_id"),
                                primary_key=True)
    proficiency        = Column(String(20), nullable=True)
    # beginner | intermediate | advanced | expert
    years_of_experience= Column(Numeric(4, 1), nullable=True)  # e.g. 1.5 years

    user  = relationship("User",  back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")


# ──────────────────────────────────────────
# 5. EDUCATION
# One user → many education entries
# ──────────────────────────────────────────

class Education(Base):
    __tablename__ = "educations"

    education_id   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    institution    = Column(String(255), nullable=False)
    degree         = Column(String(100), nullable=True)   # "B.Tech" | "M.Tech" | "BCA"
    field_of_study = Column(String(100), nullable=True)   # "Computer Science"
    start_date     = Column(Date, nullable=True)
    end_date       = Column(Date, nullable=True)          # null if currently studying
    grade          = Column(String(20), nullable=True)    # "8.5 CGPA" | "85%"

    user = relationship("User", back_populates="educations")


# ──────────────────────────────────────────
# 6. EXPERIENCE
# One user → many work experiences
# ──────────────────────────────────────────

class Experience(Base):
    __tablename__ = "experiences"

    experience_id    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id          = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    company_name     = Column(String(255), nullable=False)
    job_title        = Column(String(255), nullable=False)
    employment_type  = Column(String(50), nullable=True)
    # full_time | part_time | internship | freelance
    description      = Column(Text, nullable=True)
    start_date       = Column(Date, nullable=True)
    end_date         = Column(Date, nullable=True)
    currently_working= Column(Boolean, default=False)     # if True, end_date is null

    user = relationship("User", back_populates="experiences")


# ──────────────────────────────────────────
# 7. CERTIFICATIONS
# ──────────────────────────────────────────

class Certification(Base):
    __tablename__ = "certifications"

    certification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id          = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    name             = Column(String(255), nullable=False)   # "AWS Solutions Architect"
    issuer           = Column(String(255), nullable=True)    # "Amazon Web Services"
    issue_date       = Column(Date, nullable=True)
    expiry_date      = Column(Date, nullable=True)           # null if no expiry
    credential_url   = Column(Text, nullable=True)           # link to verify cert

    user = relationship("User", back_populates="certifications")


# ──────────────────────────────────────────
# 8. PROJECTS
# ──────────────────────────────────────────

class Project(Base):
    __tablename__ = "projects"

    project_id   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id      = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title        = Column(String(255), nullable=False)
    description  = Column(Text, nullable=True)
    github_url   = Column(Text, nullable=True)
    live_url     = Column(Text, nullable=True)
    technologies = Column(Text, nullable=True)
    # comma-separated string: "FastAPI, PostgreSQL, Docker"
    # we keep it simple — no separate join table for project techs

    user = relationship("User", back_populates="projects")


# ──────────────────────────────────────────
# 9. LANGUAGES (global lookup)
# ──────────────────────────────────────────

class Language(Base):
    __tablename__ = "languages"

    language_id = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100), unique=True, nullable=False)  # "Telugu" | "English"

    user_languages = relationship("UserLanguage", back_populates="language")


# ──────────────────────────────────────────
# 10. USER LANGUAGES
# Many-to-many: user ↔ language
# ──────────────────────────────────────────

class UserLanguage(Base):
    __tablename__ = "user_languages"
    __table_args__ = (UniqueConstraint("user_id", "language_id"),)

    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    language_id = Column(Integer, ForeignKey("languages.language_id"), primary_key=True)
    proficiency = Column(String(20), nullable=True)
    # basic | conversational | professional | native

    user     = relationship("User",     back_populates="languages")
    language = relationship("Language", back_populates="user_languages")
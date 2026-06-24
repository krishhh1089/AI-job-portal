import uuid
from sqlalchemy import (
    Column, String, Text, Boolean, Integer,
    Numeric, ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


# ──────────────────────────────────────────
# USERS
# ──────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    user_id        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name     = Column(String(100), nullable=False)
    last_name      = Column(String(100), nullable=False)
    email          = Column(String(255), unique=True, nullable=False, index=True)
    password_hash  = Column(Text, nullable=False)
    role           = Column(String(20), default="jobseeker")   # jobseeker | recruiter | admin
    profile_picture= Column(Text, nullable=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # relationships
    skills              = relationship("UserSkill", back_populates="user")
    resumes             = relationship("Resume", back_populates="user")
    applications        = relationship("JobApplication", back_populates="user")
    saved_jobs          = relationship("SavedJob", back_populates="user")
    notifications       = relationship("Notification", back_populates="user")
    refresh_tokens      = relationship("RefreshToken", back_populates="user")
    activity_logs       = relationship("ActivityLog", back_populates="user")
    job_matches         = relationship("JobMatch", back_populates="user")
    company_memberships = relationship("CompanyUser", back_populates="user")
    learning_recs       = relationship("LearningRecommendation", back_populates="user")
    mock_interviews     = relationship("MockInterview", back_populates="user")


# ──────────────────────────────────────────
# COMPANIES
# ──────────────────────────────────────────

class Company(Base):
    __tablename__ = "companies"

    company_id   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    website      = Column(Text, nullable=True)
    industry     = Column(String(100), nullable=True)
    description  = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    members = relationship("CompanyUser", back_populates="company")
    jobs    = relationship("Job", back_populates="company")


class CompanyUser(Base):
    __tablename__ = "company_users"

    company_user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id      = Column(UUID(as_uuid=True), ForeignKey("companies.company_id"), nullable=False)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    role            = Column(String(50), default="member")   # admin | member
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="members")
    user    = relationship("User", back_populates="company_memberships")


# ──────────────────────────────────────────
# SKILLS (lookup table)
# ──────────────────────────────────────────

class Skill(Base):
    __tablename__ = "skills"

    skill_id   = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), unique=True, nullable=False)

    user_skills = relationship("UserSkill", back_populates="skill")
    job_skills  = relationship("JobSkill", back_populates="skill")
    learning_recs = relationship("LearningRecommendation", back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skills"
    __table_args__ = (UniqueConstraint("user_id", "skill_id"),)

    user_id  = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)

    user  = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")


# ──────────────────────────────────────────
# JOB CATEGORIES + LOCATIONS
# ──────────────────────────────────────────

class JobCategory(Base):
    __tablename__ = "job_categories"

    category_id   = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), unique=True, nullable=False)

    jobs = relationship("Job", back_populates="category")


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    city        = Column(String(100), nullable=True)
    state       = Column(String(100), nullable=True)
    country     = Column(String(100), nullable=False)

    jobs = relationship("Job", back_populates="location")


# ──────────────────────────────────────────
# JOBS
# ──────────────────────────────────────────

class Job(Base):
    __tablename__ = "jobs"

    job_id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id       = Column(UUID(as_uuid=True), ForeignKey("companies.company_id"), nullable=False)
    category_id      = Column(Integer, ForeignKey("job_categories.category_id"), nullable=True)
    location_id      = Column(Integer, ForeignKey("locations.location_id"), nullable=True)
    title            = Column(String(255), nullable=False)
    description      = Column(Text, nullable=False)
    employment_type  = Column(String(50), nullable=False)   # full_time | part_time | internship | remote
    experience_level = Column(String(50), nullable=True)    # junior | mid | senior
    salary_min       = Column(Numeric(12, 2), nullable=True)
    salary_max       = Column(Numeric(12, 2), nullable=True)
    status           = Column(String(20), default="active")  # active | closed | draft
    posted_at        = Column(DateTime(timezone=True), server_default=func.now())
    expires_at       = Column(DateTime(timezone=True), nullable=True)

    company      = relationship("Company", back_populates="jobs")
    category     = relationship("JobCategory", back_populates="jobs")
    location     = relationship("Location", back_populates="jobs")
    skills       = relationship("JobSkill", back_populates="job")
    applications = relationship("JobApplication", back_populates="job")
    saved_by     = relationship("SavedJob", back_populates="job")
    matches      = relationship("JobMatch", back_populates="job")
    mock_interviews = relationship("MockInterview", back_populates="job")


class JobSkill(Base):
    __tablename__ = "job_skills"
    __table_args__ = (UniqueConstraint("job_id", "skill_id"),)

    job_id   = Column(UUID(as_uuid=True), ForeignKey("jobs.job_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)

    job   = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="job_skills")


# ──────────────────────────────────────────
# RESUMES
# ──────────────────────────────────────────

class Resume(Base):
    __tablename__ = "resumes"

    resume_id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id            = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    current_version_id = Column(UUID(as_uuid=True), nullable=True)   # updated after first version
    created_at         = Column(DateTime(timezone=True), server_default=func.now())

    user     = relationship("User", back_populates="resumes")
    versions = relationship("ResumeVersion", back_populates="resume",
                            foreign_keys="ResumeVersion.resume_id")


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    version_id     = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id      = Column(UUID(as_uuid=True), ForeignKey("resumes.resume_id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    file_name      = Column(String(255), nullable=False)
    file_url       = Column(Text, nullable=False)          # S3 URL
    extracted_text = Column(Text, nullable=True)           # parsed text from PDF
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    resume   = relationship("Resume", back_populates="versions",
                            foreign_keys=[resume_id])
    analysis = relationship("ResumeAnalysis", back_populates="version", uselist=False)
    analysis_history = relationship("ResumeAnalysisHistory", back_populates="version")
    applications     = relationship("JobApplication", back_populates="resume_version")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    analysis_id    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id     = Column(UUID(as_uuid=True), ForeignKey("resume_versions.version_id"),
                            unique=True, nullable=False)
    ats_score      = Column(Numeric(5, 2), nullable=True)
    strengths      = Column(Text, nullable=True)
    weaknesses     = Column(Text, nullable=True)
    ai_suggestions = Column(Text, nullable=True)
    analyzed_at    = Column(DateTime(timezone=True), server_default=func.now())

    version = relationship("ResumeVersion", back_populates="analysis")


class ResumeAnalysisHistory(Base):
    __tablename__ = "resume_analysis_history"

    history_id     = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id     = Column(UUID(as_uuid=True), ForeignKey("resume_versions.version_id"),
                            nullable=False)
    ats_score      = Column(Numeric(5, 2), nullable=True)
    strengths      = Column(Text, nullable=True)
    weaknesses     = Column(Text, nullable=True)
    ai_suggestions = Column(Text, nullable=True)
    analyzed_at    = Column(DateTime(timezone=True), server_default=func.now())

    version = relationship("ResumeVersion", back_populates="analysis_history")


# ──────────────────────────────────────────
# JOB MATCHING
# ──────────────────────────────────────────

class JobMatch(Base):
    __tablename__ = "job_matches"

    match_id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    job_id         = Column(UUID(as_uuid=True), ForeignKey("jobs.job_id"), nullable=False)
    match_score    = Column(Numeric(5, 2), nullable=True)
    missing_skills = Column(Text, nullable=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="job_matches")
    job  = relationship("Job", back_populates="matches")


# ──────────────────────────────────────────
# SAVED JOBS
# ──────────────────────────────────────────

class SavedJob(Base):
    __tablename__ = "saved_jobs"
    __table_args__ = (UniqueConstraint("user_id", "job_id"),)

    user_id  = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    job_id   = Column(UUID(as_uuid=True), ForeignKey("jobs.job_id"), primary_key=True)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="saved_jobs")
    job  = relationship("Job", back_populates="saved_by")


# ──────────────────────────────────────────
# APPLICATIONS
# ──────────────────────────────────────────

class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    job_id         = Column(UUID(as_uuid=True), ForeignKey("jobs.job_id"), nullable=False)
    version_id     = Column(UUID(as_uuid=True), ForeignKey("resume_versions.version_id"),
                            nullable=True)
    current_status = Column(String(50), default="applied")
    # applied | under_review | shortlisted | rejected | hired
    applied_at     = Column(DateTime(timezone=True), server_default=func.now())

    user           = relationship("User", back_populates="applications")
    job            = relationship("Job", back_populates="applications")
    resume_version = relationship("ResumeVersion", back_populates="applications")
    status_history = relationship("ApplicationStatusHistory", back_populates="application")


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    status_history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id    = Column(UUID(as_uuid=True),
                               ForeignKey("job_applications.application_id"), nullable=False)
    old_status        = Column(String(50), nullable=True)
    new_status        = Column(String(50), nullable=False)
    changed_at        = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("JobApplication", back_populates="status_history")


# ──────────────────────────────────────────
# NOTIFICATIONS
# ──────────────────────────────────────────

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title           = Column(String(255), nullable=False)
    message         = Column(Text, nullable=False)
    is_read         = Column(Boolean, default=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notifications")


# ──────────────────────────────────────────
# ACTIVITY LOGS
# ──────────────────────────────────────────

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    log_id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    action_type = Column(String(100), nullable=False)   # e.g. "applied", "saved_job"
    entity_type = Column(String(100), nullable=True)    # e.g. "job", "resume"
    entity_id   = Column(UUID(as_uuid=True), nullable=True)
    description = Column(Text, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="activity_logs")


# ──────────────────────────────────────────
# REFRESH TOKENS (for JWT)
# ──────────────────────────────────────────

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token_id   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    token      = Column(Text, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")


# ──────────────────────────────────────────
# LEARNING RECOMMENDATIONS
# ──────────────────────────────────────────

class LearningRecommendation(Base):
    __tablename__ = "learning_recommendations"

    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id           = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    skill_id          = Column(Integer, ForeignKey("skills.skill_id"), nullable=False)
    course_name       = Column(String(255), nullable=False)
    course_url        = Column(Text, nullable=True)
    created_at        = Column(DateTime(timezone=True), server_default=func.now())

    user  = relationship("User", back_populates="learning_recs")
    skill = relationship("Skill", back_populates="learning_recs")


# ──────────────────────────────────────────
# MOCK INTERVIEWS
# ──────────────────────────────────────────

class MockInterview(Base):
    __tablename__ = "mock_interviews"

    interview_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id      = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    job_id       = Column(UUID(as_uuid=True), ForeignKey("jobs.job_id"), nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    user    = relationship("User", back_populates="mock_interviews")
    job     = relationship("Job", back_populates="mock_interviews")
    results = relationship("InterviewResult", back_populates="interview")


class InterviewResult(Base):
    __tablename__ = "interview_results"

    result_id    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("mock_interviews.interview_id"),
                          nullable=False)
    score        = Column(Numeric(5, 2), nullable=True)
    feedback     = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    interview = relationship("MockInterview", back_populates="results")
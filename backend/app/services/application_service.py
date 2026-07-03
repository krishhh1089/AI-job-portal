from uuid import UUID

from sqlalchemy.orm import Session

from app.models.application import (
    Application,
    ApplicationStatus
)
from app.models.jobs import JobStatus
from app.models.user import User, UserRole

from app.repositories.application_repository import (
    application_repository
)
from app.repositories.job_repository import (
    job_repository
)
from app.repositories.resume_repository import (
    resume_repository
)

from app.schemas.application import (
    CreateApplicationRequest,
    UpdateApplicationStatusRequest
)

from app.models.application import Application, ApplicationStatus

class ApplicationService:

    # =====================================
    # APPLY FOR JOB
    # =====================================

    @staticmethod
    def create_application(
        db: Session,
        application_data: CreateApplicationRequest,
        current_user: User
    ) -> Application:

        # -----------------------------
        # Only jobseekers can apply
        # -----------------------------

        if current_user.role != UserRole.JOBSEEKER:
            raise ValueError(
                "Only jobseekers can apply for jobs."
            )

        # -----------------------------
        # Job exists
        # -----------------------------

        job = job_repository.get_by_id(
            db,
            application_data.job_id
        )

        if job is None:
            raise ValueError(
                "Job not found."
            )

        # -----------------------------
        # Job is active
        # -----------------------------

        if job.status != JobStatus.ACTIVE:
            raise ValueError(
                "This job is no longer accepting applications."
            )
        
        # -----------------------------
        # Resume exists
        # -----------------------------

        resume = resume_repository.get_resume_by_id(
            db,
            application_data.resume_id
        )

        if resume is None:
            raise ValueError(
                "Resume not found."
            )

        # -----------------------------
        # Resume belongs to user
        # -----------------------------

        if resume.user_id != current_user.user_id:
            raise ValueError(
                "You can only use your own resume."
            )

        # -----------------------------
        # Already applied
        # -----------------------------

        existing_application = (
            application_repository.get_by_user_and_job(
                db,
                current_user.user_id,
                application_data.job_id
            )
        )

        if existing_application:
            raise ValueError(
                "You have already applied for this job."
            )

        # -----------------------------
        # Create application
        # -----------------------------

        application = Application(
            job_id=application_data.job_id,
            user_id=current_user.user_id,
            resume_id=application_data.resume_id,
            cover_letter=application_data.cover_letter,
            status=ApplicationStatus.APPLIED
        )

        return application_repository.create(
            db,
            application
        )

    # =====================================
    # GET APPLICATION
    # =====================================

    @staticmethod
    def get_application_by_id(
        db: Session,
        application_id: UUID
    ) -> Application | None:

        return application_repository.get_by_id(
            db,
            application_id
        )

    # =====================================
    # MY APPLICATIONS
    # =====================================

    @staticmethod
    def get_my_applications(
        db: Session,
        current_user: User
    ) -> list[Application]:

        if current_user.role != UserRole.JOBSEEKER:
            raise ValueError(
                "Only jobseekers can view their applications."
            )

        return application_repository.get_by_user(
            db,
            current_user.user_id
        )
    # =====================================
    # JOB APPLICATIONS
    # =====================================

    @staticmethod
    def get_job_applications(
        db: Session,
        job_id: UUID,
        recruiter: User
    ) -> list[Application]:

        if recruiter.role != UserRole.RECRUITER:
            raise ValueError(
                "Only recruiters can view applications."
            )

        job = job_repository.get_by_id(
            db,
            job_id
        )

        if job is None:
            raise ValueError(
                "Job not found."
            )

        if job.company_id != recruiter.company_id:
            raise ValueError(
                "You can only view applications for your company's jobs."
            )

        return application_repository.get_by_job(
            db,
            job_id
        )

    # =====================================
    # UPDATE STATUS
    # =====================================

    @staticmethod
    def update_status(
        db: Session,
        application_id: UUID,
        application_data: UpdateApplicationStatusRequest,
        recruiter: User
    ) -> Application:

        if recruiter.role != UserRole.RECRUITER:
            raise ValueError(
                "Only recruiters can update application status."
            )

        application = application_repository.get_by_id(
            db,
            application_id
        )

        if application is None:
            raise ValueError(
                "Application not found."
            )

        if application.job.company_id != recruiter.company_id:
            raise ValueError(
                "You can update only your company's applications."
            )

        allowed_statuses = {
            ApplicationStatus.REVIEWING,
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.HIRED
        }

        if application_data.status not in allowed_statuses:
            raise ValueError(
                "Recruiters can only set status to Reviewing, Shortlisted, Rejected, or Hired."
            )

        application.status = application_data.status

        return application_repository.update(
            db,
            application
        )

    # =====================================
    # WITHDRAW APPLICATION
    # =====================================

    @staticmethod
    def withdraw_application(
        db: Session,
        application_id: UUID,
        current_user: User
    ) -> Application:

        application = application_repository.get_by_id(
            db,
            application_id
        )

        if application is None:
            raise ValueError(
                "Application not found."
            )

        if application.user_id != current_user.user_id:
            raise ValueError(
                "You can withdraw only your own application."
            )

        application.status = (
            ApplicationStatus.WITHDRAWN
        )

        return application_repository.update(
            db,
            application
        )
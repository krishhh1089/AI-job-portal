from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    NotFoundException
)

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

        if current_user.role != UserRole.JOBSEEKER:
            raise ForbiddenException(
                "Only jobseekers can apply for jobs."
            )

        job = job_repository.get_by_id(
            db,
            application_data.job_id
        )

        if job is None:
            raise NotFoundException(
                "Job not found."
            )

        if job.status != JobStatus.ACTIVE:
            raise BadRequestException(
                "This job is no longer accepting applications."
            )

        resume = resume_repository.get_resume_by_id(
            db,
            application_data.resume_id
        )

        if resume is None:
            raise NotFoundException(
                "Resume not found."
            )

        if resume.user_id != current_user.user_id:
            raise ForbiddenException(
                "You can only use your own resume."
            )

        existing_application = (
            application_repository.get_by_user_and_job(
                db,
                current_user.user_id,
                application_data.job_id
            )
        )

        if existing_application:
            raise ConflictException(
                "You have already applied for this job."
            )

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
        application_id: UUID,
        current_user: User
    ) -> Application:

        application = application_repository.get_by_id(
            db,
            application_id
        )

        if application is None:
            raise NotFoundException(
                "Application not found."
            )

        if application.user_id != current_user.user_id:
            raise ForbiddenException(
                "You can view only your own application."
            )

        return application

    # =====================================
    # MY APPLICATIONS
    # =====================================

    @staticmethod
    def get_my_applications(
        db: Session,
        current_user: User,
        limit: int = 20,
        cursor: str | None = None,
        status: ApplicationStatus | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        if current_user.role != UserRole.JOBSEEKER:
            raise ForbiddenException(
                "Only jobseekers can view their applications."
            )

        return application_repository.get_by_user(
            db=db,
            user_id=current_user.user_id,
            limit=limit,
            cursor=cursor,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )

    # =====================================
    # JOB APPLICATIONS
    # =====================================

    @staticmethod
    def get_job_applications(
        db: Session,
        job_id: UUID,
        recruiter: User,
        limit: int = 20,
        cursor: str | None = None,
        status: ApplicationStatus | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        if recruiter.role != UserRole.RECRUITER:
            raise ForbiddenException(
                "Only recruiters can view applications."
            )

        job = job_repository.get_by_id(
            db,
            job_id
        )

        if job is None:
            raise NotFoundException(
                "Job not found."
            )

        if job.company_id != recruiter.company_id:
            raise ForbiddenException(
                "You can only view applications for your company's jobs."
            )

        return application_repository.get_by_job(
            db=db,
            job_id=job_id,
            limit=limit,
            cursor=cursor,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
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
            raise ForbiddenException(
                "Only recruiters can update application status."
            )

        application = application_repository.get_by_id(
            db,
            application_id
        )

        if application is None:
            raise NotFoundException(
                "Application not found."
            )

        if application.job.company_id != recruiter.company_id:
            raise ForbiddenException(
                "You can update only your company's applications."
            )

        allowed_statuses = {
            ApplicationStatus.REVIEWING,
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.HIRED
        }

        if application_data.status not in allowed_statuses:
            raise BadRequestException(
                "Recruiters can only set status to Reviewing, "
                "Shortlisted, Rejected, or Hired."
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
            raise NotFoundException(
                "Application not found."
            )

        if application.user_id != current_user.user_id:
            raise ForbiddenException(
                "You can withdraw only your own application."
            )

        if application.status == ApplicationStatus.WITHDRAWN:
            raise BadRequestException(
                "Application is already withdrawn."
            )

        if application.status == ApplicationStatus.HIRED:
            raise BadRequestException(
                "A hired application cannot be withdrawn."
            )

        application.status = ApplicationStatus.WITHDRAWN

        return application_repository.update(
            db,
            application
        )
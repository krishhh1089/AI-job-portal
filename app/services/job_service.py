from uuid import UUID

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.user import User, UserRole

from app.repositories.job_repository import (
    job_repository
)

from app.schemas.job import (
    CreateJobRequest,
    UpdateJobRequest
)


class JobService:

    # =====================================
    # CREATE
    # =====================================

    @staticmethod
    def create_job(
        db: Session,
        job_data: CreateJobRequest,
        recruiter: User
    ) -> Job:

        # ---------------------------------
        # Only recruiters can create jobs
        # ---------------------------------

        if recruiter.role != UserRole.RECRUITER:
            raise ValueError(
                "Only recruiters can create jobs."
            )

        # ---------------------------------
        # Recruiter must belong to company
        # ---------------------------------

        if recruiter.company_id is None:
            raise ValueError(
                "Recruiter is not assigned to a company."
            )

        # ---------------------------------
        # Create Job
        # ---------------------------------

        job_dict = job_data.model_dump(
        exclude={"skill_ids"}
        )

        job = Job(
            **job_dict,
            company_id=recruiter.company_id,
            posted_by=recruiter.user_id
        )

        job = job_repository.create(
            db,
            job
        )

        # ---------------------------------
        # Job Skills
        # ---------------------------------

        # Will be implemented
        # after JobSkill table

        return job

    # =====================================
    # READ
    # =====================================

    @staticmethod
    def get_job_by_id(
        db: Session,
        job_id: UUID
    ) -> Job | None:

        return job_repository.get_by_id(
            db,
            job_id
        )

    @staticmethod
    def get_all_jobs(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Job]:

        return job_repository.get_all(
            db,
            skip,
            limit
        )

    # =====================================
    # UPDATE
    # =====================================

    @staticmethod
    def update_job(
        db: Session,
        job: Job,
        job_data: UpdateJobRequest
    ) -> Job:

        update_data = job_data.model_dump(
            exclude_unset=True
        )

        update_data.pop(
            "skill_ids",
            None
        )

        for field, value in update_data.items():
            setattr(
                job,
                field,
                value
            )

        return job_repository.update(
            db,
            job
        )

    # =====================================
    # DELETE
    # =====================================

    @staticmethod
    def delete_job(
        db: Session,
        job: Job
    ) -> None:

        job_repository.delete(
            db,
            job
        )
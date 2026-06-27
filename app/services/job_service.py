# app/services/job_service.py

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.jobs import Job
from app.models.job_skill import JobSkill
from app.models.user import User, UserRole

from app.repositories.job_repository import job_repository
from app.repositories.skill_repository import skill_repository
from app.repositories.job_skill_repository import job_skill_repository

from app.schemas.jobs import CreateJobRequest, UpdateJobRequest


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

        if recruiter.role != UserRole.RECRUITER:
            raise ValueError("Only recruiters can create jobs.")

        if recruiter.company_id is None:
            raise ValueError("Recruiter is not assigned to a company.")

        for skill_id in job_data.skill_ids:
            skill = skill_repository.get_by_id(
                db,
                skill_id
            )

            if skill is None:
                raise ValueError("Invalid skill id.")

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

        for skill_id in job_data.skill_ids:
            job_skill = JobSkill(
                job_id=job.job_id,
                skill_id=skill_id
            )

            job_skill_repository.create(
                db,
                job_skill
            )

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
        job_id: UUID,
        job_data: UpdateJobRequest,
        recruiter: User
    ) -> Job:

        job = job_repository.get_by_id(
            db,
            job_id
        )

        if job is None:
            raise ValueError("Job not found.")

        if recruiter.role != UserRole.RECRUITER:
            raise ValueError("Only recruiters can update jobs.")

        if job.company_id != recruiter.company_id:
            raise ValueError("You can update only your company's jobs.")

        update_data = job_data.model_dump(
            exclude_unset=True
        )

        skill_ids = update_data.pop(
            "skill_ids",
            None
        )

        for field, value in update_data.items():
            setattr(
                job,
                field,
                value
            )

        job = job_repository.update(
            db,
            job
        )

        if skill_ids is not None:

            for skill_id in skill_ids:
                skill = skill_repository.get_by_id(
                    db,
                    skill_id
                )

                if skill is None:
                    raise ValueError("Invalid skill id.")

            job_skill_repository.delete_by_job(
                db,
                job.job_id
            )

            for skill_id in skill_ids:
                job_skill = JobSkill(
                    job_id=job.job_id,
                    skill_id=skill_id
                )

                job_skill_repository.create(
                    db,
                    job_skill
                )

        return job
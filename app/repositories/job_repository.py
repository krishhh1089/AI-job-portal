from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.jobs import Job


class JobRepository:

    # =====================================
    # CREATE
    # =====================================

    def create(
        self,
        db: Session,
        job: Job
    ) -> Job:

        try:
            db.add(job)
            db.commit()
            db.refresh(job)

            return job

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # READ
    # =====================================

    def get_by_id(
        self,
        db: Session,
        job_id: UUID
    ) -> Job | None:

        return (
            db.query(Job)
            .filter(Job.job_id == job_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Job]:

        return (
            db.query(Job)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # =====================================
    # UPDATE
    # =====================================

    def update(
        self,
        db: Session,
        job: Job
    ) -> Job:

        try:
            db.commit()
            db.refresh(job)

            return job

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # DELETE
    # =====================================

    def delete(
        self,
        db: Session,
        job: Job
    ) -> None:

        try:
            db.delete(job)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================

job_repository = JobRepository()
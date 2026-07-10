import datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from streamlit import json

from app.models.jobs import Job, JobStatus
import base64
import json
from sqlalchemy import or_, and_, desc


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

    # def get_all(
    #     self,
    #     db: Session,
    #     skip: int = 0,
    #     limit: int = 100
    # ) -> list[Job]:

    #     return (
    #         db.query(Job)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

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


    def deactivate(
        self,
        db: Session,
        job: Job
    ) -> Job:

        try:
            job.status = JobStatus.CLOSED

            db.commit()
            db.refresh(job)

            return job

        except SQLAlchemyError:
            db.rollback()
            raise
    
    @staticmethod
    def delete_job(
        db: Session,
        job: Job
    ) -> Job:

        return job_repository.deactivate(
            db,
            job
        )
    

    def encode_cursor(self, created_at: datetime, job_id: UUID) -> str:
        data = {
            "created_at": created_at.isoformat(),
            "job_id": str(job_id)
        }

        return base64.urlsafe_b64encode(
            json.dumps(data).encode()
        ).decode()
    

    def decode_cursor(self, cursor: str):
        data = json.loads(
            base64.urlsafe_b64decode(cursor.encode()).decode()
        )

        return {
            "created_at": datetime.fromisoformat(data["created_at"]),
            "job_id": UUID(data["job_id"])
        }
    
    def get_all_cursor(
        self,
        db: Session,
        limit: int = 10,
        cursor: str | None = None
    ):
        query = db.query(Job)

        if cursor:
            cursor_data = self.decode_cursor(cursor)

            query = query.filter(
                or_(
                    Job.created_at < cursor_data["created_at"],
                    and_(
                        Job.created_at == cursor_data["created_at"],
                        Job.job_id < cursor_data["job_id"]
                    )
                )
            )

        jobs = (
            query
            .order_by(desc(Job.created_at), desc(Job.job_id))
            .limit(limit + 1)
            .all()
        )

        has_more = len(jobs) > limit
        jobs = jobs[:limit]

        next_cursor = None

        if has_more:
            last_job = jobs[-1]
            next_cursor = self.encode_cursor(
                last_job.created_at,
                last_job.job_id
            )

        return {
            "limit": limit,
            "next_cursor": next_cursor,
            "jobs": jobs
        }


job_repository = JobRepository()
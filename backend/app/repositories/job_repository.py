import datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from streamlit import json

from app.models.jobs import Job, JobStatus
import base64
import json
from sqlalchemy import and_, asc, desc, func, or_
from app.utils.cursor import encode_cursor, decode_cursor


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
    

    def get_all(
        self,
        db: Session,
        limit: int = 20,
        cursor: str | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        query = db.query(Job)

        # ---------------------------------
        # 1. Searching
        # ---------------------------------

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Job.title.ilike(search_value),
                    Job.description.ilike(search_value),
                    Job.location.ilike(search_value)
                )
            )

        # ---------------------------------
        # 2. Allowed sorting fields
        # ---------------------------------

        allowed_sort_fields = {
            "created_at": Job.created_at,
            "title": Job.title,

            # Salary may be NULL.
            # COALESCE converts NULL into 0.
            "salary_min": func.coalesce(
                Job.salary_min,
                0
            ),

            "salary_max": func.coalesce(
                Job.salary_max,
                0
            )
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Job.created_at
        )

        # ---------------------------------
        # 3. Cursor filtering
        # ---------------------------------

        if cursor:
            cursor_data = decode_cursor(cursor)

            cursor_sort_by = cursor_data["sort_by"]
            cursor_sort_order = cursor_data["sort_order"]
            cursor_sort_value = cursor_data["sort_value"]
            cursor_job_id = cursor_data["record_id"]

            # Cursor must belong to the same sorting request
            if cursor_sort_by != sort_by:
                raise ValueError(
                    "Cursor does not match sort_by"
                )

            if cursor_sort_order != sort_order:
                raise ValueError(
                    "Cursor does not match sort_order"
                )

            # Convert datetime string back to datetime
            if sort_by == "created_at":
                cursor_sort_value = datetime.fromisoformat(
                    cursor_sort_value
                )

            if sort_by in {"salary_min", "salary_max"}:
                cursor_sort_value = int(cursor_sort_value)

            # Descending:
            # values smaller than the cursor come next
            if sort_order == "desc":
                query = query.filter(
                    or_(
                        sort_column < cursor_sort_value,

                        and_(
                            sort_column == cursor_sort_value,
                            Job.job_id < cursor_job_id
                        )
                    )
                )

            # Ascending:
            # values greater than the cursor come next
            else:
                query = query.filter(
                    or_(
                        sort_column > cursor_sort_value,

                        and_(
                            sort_column == cursor_sort_value,
                            Job.job_id > cursor_job_id
                        )
                    )
                )

        # ---------------------------------
        # 4. Apply sorting
        # ---------------------------------

        if sort_order == "asc":
            query = query.order_by(
                asc(sort_column),
                asc(Job.job_id)
            )

        else:
            query = query.order_by(
                desc(sort_column),
                desc(Job.job_id)
            )

        # Fetch one extra record
        jobs = query.limit(limit + 1).all()

        has_next = len(jobs) > limit

        # Remove the extra record
        jobs = jobs[:limit]

        next_cursor = None

        # ---------------------------------
        # 5. Create next cursor
        # ---------------------------------

        if has_next and jobs:
            last_job = jobs[-1]

            if sort_by == "created_at":
                last_sort_value = last_job.created_at

            elif sort_by == "title":
                last_sort_value = last_job.title

            elif sort_by == "salary_min":
                last_sort_value = last_job.salary_min or 0

            else:
                last_sort_value = last_job.salary_max or 0

            next_cursor = encode_cursor(
                sort_value=last_sort_value,
                record_id=last_job.job_id,
                sort_by=sort_by,
                sort_order=sort_order
            )

        return {
            "items": jobs,
            "next_cursor": next_cursor,
            "has_next": has_next
        }


job_repository = JobRepository()
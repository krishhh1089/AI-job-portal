from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BadRequestException
from app.models.application import (
    Application,
    ApplicationStatus
)
from app.utils.cursor import decode_cursor, encode_cursor


class ApplicationRepository:

    # =====================================
    # CREATE
    # =====================================

    def create(
        self,
        db: Session,
        application: Application
    ) -> Application:

        try:
            db.add(application)
            db.commit()
            db.refresh(application)

            return application

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # GET BY ID
    # =====================================

    def get_by_id(
        self,
        db: Session,
        application_id: UUID
    ) -> Application | None:

        return (
            db.query(Application)
            .filter(
                Application.application_id == application_id
            )
            .first()
        )

    # =====================================
    # PAGINATED APPLICATION QUERY
    # =====================================

    def _get_paginated(
        self,
        query,
        limit: int = 20,
        cursor: str | None = None,
        status: ApplicationStatus | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        # -----------------------------
        # STATUS FILTER
        # -----------------------------

        if status is not None:
            query = query.filter(
                Application.status == status
            )

        # -----------------------------
        # ALLOWED SORT FIELDS
        # -----------------------------

        allowed_sort_fields = {
            "created_at": Application.created_at,
            "updated_at": Application.updated_at
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Application.created_at
        )

        # -----------------------------
        # CURSOR FILTER
        # -----------------------------

        if cursor:
            cursor_data = decode_cursor(cursor)

            cursor_sort_value = cursor_data["sort_value"]
            cursor_application_id = cursor_data["record_id"]

            if cursor_data["sort_by"] != sort_by:
                raise BadRequestException(
                    "Cursor does not match sort_by."
                )

            if cursor_data["sort_order"] != sort_order:
                raise BadRequestException(
                    "Cursor does not match sort_order."
                )

            # created_at and updated_at are datetime fields.
            try:
                cursor_sort_value = datetime.fromisoformat(
                    cursor_sort_value
                )
            except (TypeError, ValueError) as exc:
                raise BadRequestException(
                    "Invalid application cursor."
                ) from exc

            if sort_order == "desc":
                query = query.filter(
                    or_(
                        sort_column < cursor_sort_value,
                        and_(
                            sort_column == cursor_sort_value,
                            Application.application_id
                            < cursor_application_id
                        )
                    )
                )

            else:
                query = query.filter(
                    or_(
                        sort_column > cursor_sort_value,
                        and_(
                            sort_column == cursor_sort_value,
                            Application.application_id
                            > cursor_application_id
                        )
                    )
                )

        # -----------------------------
        # APPLY SORTING
        # -----------------------------

        if sort_order == "asc":
            query = query.order_by(
                asc(sort_column),
                asc(Application.application_id)
            )

        else:
            query = query.order_by(
                desc(sort_column),
                desc(Application.application_id)
            )

        # Fetch one additional application.
        applications = query.limit(limit + 1).all()

        has_next = len(applications) > limit

        # Remove extra application before returning.
        applications = applications[:limit]

        next_cursor = None

        # -----------------------------
        # CREATE NEXT CURSOR
        # -----------------------------

        if has_next and applications:
            last_application = applications[-1]

            if sort_by == "updated_at":
                last_sort_value = last_application.updated_at
            else:
                last_sort_value = last_application.created_at

            next_cursor = encode_cursor(
                sort_value=last_sort_value,
                record_id=last_application.application_id,
                sort_by=sort_by,
                sort_order=sort_order
            )

        return {
            "items": applications,
            "next_cursor": next_cursor,
            "has_next": has_next
        }

    # =====================================
    # GET BY USER
    # =====================================

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
        limit: int = 20,
        cursor: str | None = None,
        status: ApplicationStatus | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        query = (
            db.query(Application)
            .filter(
                Application.user_id == user_id
            )
        )

        return self._get_paginated(
            query=query,
            limit=limit,
            cursor=cursor,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )

    # =====================================
    # GET BY JOB
    # =====================================

    def get_by_job(
        self,
        db: Session,
        job_id: UUID,
        limit: int = 20,
        cursor: str | None = None,
        status: ApplicationStatus | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        query = (
            db.query(Application)
            .filter(
                Application.job_id == job_id
            )
        )

        return self._get_paginated(
            query=query,
            limit=limit,
            cursor=cursor,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )

    # =====================================
    # CHECK DUPLICATE APPLICATION
    # =====================================

    def get_by_user_and_job(
        self,
        db: Session,
        user_id: UUID,
        job_id: UUID
    ) -> Application | None:

        return (
            db.query(Application)
            .filter(
                Application.user_id == user_id,
                Application.job_id == job_id
            )
            .first()
        )

    # =====================================
    # UPDATE
    # =====================================

    def update(
        self,
        db: Session,
        application: Application
    ) -> Application:

        try:
            db.commit()
            db.refresh(application)

            return application

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # DELETE
    # =====================================

    def delete(
        self,
        db: Session,
        application: Application
    ) -> None:

        try:
            db.delete(application)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise


application_repository = ApplicationRepository()
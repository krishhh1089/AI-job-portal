from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.application import Application


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
    # GET BY USER
    # =====================================

    def get_by_user(
        self,
        db: Session,
        user_id: UUID
    ) -> list[Application]:

        return (
            db.query(Application)
            .filter(
                Application.user_id == user_id
            )
            .all()
        )

    # =====================================
    # GET BY JOB
    # =====================================

    def get_by_job(
        self,
        db: Session,
        job_id: UUID
    ) -> list[Application]:

        return (
            db.query(Application)
            .filter(
                Application.job_id == job_id
            )
            .all()
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
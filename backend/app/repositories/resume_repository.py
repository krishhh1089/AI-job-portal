from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    def create(
        self,
        db: Session,
        resume: Resume
    ) -> Resume:
        try:
            db.add(resume)
            db.commit()
            db.refresh(resume)
            return resume

        except SQLAlchemyError:
            db.rollback()
            raise

    def get_resume_by_id(
        self,
        db: Session,
        resume_id: UUID
    ) -> Resume | None:

        return (
            db.query(Resume)
            .filter(Resume.resume_id == resume_id)
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: UUID
    ) -> list[Resume]:

        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .all()
        )

    def unset_default_for_user(
        self,
        db: Session,
        user_id: UUID
    ) -> None:
        try:
            (
                db.query(Resume)
                .filter(Resume.user_id == user_id)
                .update({Resume.is_default: False})
            )

            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise

    def update(
        self,
        db: Session,
        resume: Resume
    ) -> Resume:
        try:
            db.commit()
            db.refresh(resume)
            return resume

        except SQLAlchemyError:
            db.rollback()
            raise

    def delete(
        self,
        db: Session,
        resume: Resume
    ) -> None:
        try:
            db.delete(resume)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise


resume_repository = ResumeRepository()
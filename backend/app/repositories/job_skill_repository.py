from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.job_skill import JobSkill


class JobSkillRepository:

    # =====================================
    # CREATE
    # =====================================

    def create(
        self,
        db: Session,
        job_skill: JobSkill
    ) -> JobSkill:

        try:
            db.add(job_skill)
            db.commit()
            db.refresh(job_skill)

            return job_skill

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # DELETE ALL SKILLS OF A JOB
    # =====================================

    def delete_by_job(
        self,
        db: Session,
        job_id
    ) -> None:

        try:
            (
                db.query(JobSkill)
                .filter(JobSkill.job_id == job_id)
                .delete()
            )

            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise


job_skill_repository = JobSkillRepository()
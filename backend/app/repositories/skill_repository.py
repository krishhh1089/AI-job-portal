from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.skill import Skill


class SkillRepository:

    # =====================================
    # CREATE
    # =====================================

    def create(
        self,
        db: Session,
        skill: Skill
    ) -> Skill:
        try:
            db.add(skill)
            db.commit()
            db.refresh(skill)

            return skill

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # READ
    # =====================================

    def get_by_id(
        self,
        db: Session,
        skill_id: UUID
    ) -> Skill | None:

        return (
            db.query(Skill)
            .filter(Skill.skill_id == skill_id)
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        name: str
    ) -> Skill | None:

        return (
            db.query(Skill)
            .filter(Skill.name == name)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Skill]:

        return (
            db.query(Skill)
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
        skill: Skill
    ) -> Skill:
        try:
            db.commit()
            db.refresh(skill)

            return skill

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # DELETE
    # =====================================

    def delete(
        self,
        db: Session,
        skill: Skill
    ) -> None:
        try:
            db.delete(skill)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise


# Singleton Instance

skill_repository = SkillRepository()
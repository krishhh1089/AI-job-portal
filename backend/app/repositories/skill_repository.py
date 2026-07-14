from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_

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
    search: str | None = None,
    sort_by: str = "name",
    sort_order: str = "asc",
    limit: int = 100
) -> list[Skill]:

        query = db.query(Skill)

        # =====================================
        # SEARCH
        # =====================================

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Skill.name.ilike(search_value),
                    Skill.category.ilike(search_value)
                )
            )

        # =====================================
        # ALLOWED SORT FIELDS
        # =====================================

        allowed_sort_fields = {
            "name": Skill.name,
            "category": Skill.category,
            "created_at": Skill.created_at
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Skill.name
        )

        # =====================================
        # APPLY SORTING
        # =====================================

        if sort_order == "desc":
            query = query.order_by(
                desc(sort_column),
                desc(Skill.skill_id)
            )

        else:
            query = query.order_by(
                asc(sort_column),
                asc(Skill.skill_id)
            )

        return query.limit(limit).all()

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
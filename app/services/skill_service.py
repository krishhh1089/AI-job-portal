from uuid import UUID

from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.repositories.skill_repository import skill_repository
from app.schemas.skill import (
    CreateSkillRequest,
    UpdateSkillRequest
)


class SkillService:

    # =====================================
    # CREATE
    # =====================================

    @staticmethod
    def create_skill(
        db: Session,
        skill_data: CreateSkillRequest
    ) -> Skill:

        skill_name = skill_data.name.lower().strip()

        existing_skill = skill_repository.get_by_name(
            db,
            skill_name
        )

        if existing_skill:
            raise ValueError(
                "Skill already exists."
            )

        skill = Skill(
            name=skill_name,
            category=skill_data.category
        )
    
        return skill_repository.create(
            db,
            skill
        )

    # =====================================
    # READ
    # =====================================

    @staticmethod
    def get_skill_by_id(
        db: Session,
        skill_id: UUID
    ) -> Skill | None:

        return skill_repository.get_by_id(
            db,
            skill_id
        )

    @staticmethod
    def get_all_skills(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Skill]:

        return skill_repository.get_all(
            db,
            skip,
            limit
        )

    # =====================================
    # UPDATE
    # =====================================

    @staticmethod
    def update_skill(
        db: Session,
        skill: Skill,
        skill_data: UpdateSkillRequest
    ) -> Skill:

        update_data = skill_data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            update_data["name"] = (
                update_data["name"]
                .lower()
                .strip()
            )

        for field, value in update_data.items():
            setattr(
                skill,
                field,
                value
            )

        return skill_repository.update(
            db,
            skill
        )

    # =====================================
    # DELETE
    # =====================================

    @staticmethod
    def delete_skill(
        db: Session,
        skill: Skill
    ) -> None:

        skill_repository.delete(
            db,
            skill
        )
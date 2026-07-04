# app/services/skill_service.py

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.models.user import User, UserRole

from app.repositories.skill_repository import skill_repository

from app.schemas.skill import (
    CreateSkillRequest,
    UpdateSkillRequest
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    ConflictException
)


class SkillService:

    @staticmethod
    def create_skill(
        db: Session,
        skill_data: CreateSkillRequest,
        current_user: User
    ) -> Skill:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException(
                "Only admin can create skills."
            )

        skill_name = skill_data.name.lower().strip()

        existing_skill = skill_repository.get_by_name(
            db=db,
            name=skill_name
        )

        if existing_skill:
            raise ConflictException(
                "Skill already exists."
            )

        skill = Skill(
            name=skill_name,
            category=skill_data.category
        )

        return skill_repository.create(
            db=db,
            skill=skill
        )

    @staticmethod
    def get_skill_by_id(
        db: Session,
        skill_id: UUID
    ) -> Skill:

        skill = skill_repository.get_by_id(
            db=db,
            skill_id=skill_id
        )

        if skill is None:
            raise NotFoundException(
                "Skill not found."
            )

        return skill

    @staticmethod
    def get_all_skills(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Skill]:

        return skill_repository.get_all(
            db=db,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def update_skill(
        db: Session,
        skill_id: UUID,
        skill_data: UpdateSkillRequest,
        current_user: User
    ) -> Skill:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException(
                "Only admin can update skills."
            )

        skill = skill_repository.get_by_id(
            db=db,
            skill_id=skill_id
        )

        if skill is None:
            raise NotFoundException(
                "Skill not found."
            )

        update_data = skill_data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise BadRequestException(
                "No data provided for update."
            )

        if "name" in update_data:
            update_data["name"] = (
                update_data["name"]
                .lower()
                .strip()
            )

            existing_skill = skill_repository.get_by_name(
                db=db,
                name=update_data["name"]
            )

            if existing_skill and existing_skill.skill_id != skill.skill_id:
                raise ConflictException(
                    "Skill already exists."
                )

        for field, value in update_data.items():
            setattr(skill, field, value)

        return skill_repository.update(
            db=db,
            skill=skill
        )

    @staticmethod
    def delete_skill(
        db: Session,
        skill_id: UUID,
        current_user: User
    ) -> None:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException(
                "Only admin can delete skills."
            )

        skill = skill_repository.get_by_id(
            db=db,
            skill_id=skill_id
        )

        if skill is None:
            raise NotFoundException(
                "Skill not found."
            )

        skill_repository.delete(
            db=db,
            skill=skill
        )


skill_service = SkillService()
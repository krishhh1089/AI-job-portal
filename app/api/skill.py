from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User, UserRole
from app.schemas.skill import (
    CreateSkillRequest,
    UpdateSkillRequest,
    SkillResponse
)
from app.services.skill_service import SkillService


router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


@router.post(
    "/",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED
)
def create_skill(
    skill_data: CreateSkillRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create skills."
        )

    try:
        return SkillService.create_skill(
            db,
            skill_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[SkillResponse]
)
def get_all_skills(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return SkillService.get_all_skills(
        db,
        skip,
        limit
    )


@router.get(
    "/{skill_id}",
    response_model=SkillResponse
)
def get_skill_by_id(
    skill_id: UUID,
    db: Session = Depends(get_db)
):
    skill = SkillService.get_skill_by_id(
        db,
        skill_id
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found."
        )

    return skill


@router.patch(
    "/{skill_id}",
    response_model=SkillResponse
)
def update_skill(
    skill_id: UUID,
    skill_data: UpdateSkillRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update skills."
        )

    skill = SkillService.get_skill_by_id(
        db,
        skill_id
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found."
        )

    try:
        return SkillService.update_skill(
            db,
            skill,
            skill_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_skill(
    skill_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete skills."
        )

    skill = SkillService.get_skill_by_id(
        db,
        skill_id
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found."
        )

    SkillService.delete_skill(
        db,
        skill
    )
# app/routers/skill_router.py

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User

from app.schemas.skill import (
    CreateSkillRequest,
    UpdateSkillRequest,
    SkillResponse
)

from app.services.skill_service import skill_service


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
    return skill_service.create_skill(
        db=db,
        skill_data=skill_data,
        current_user=current_user
    )


@router.get(
    "",
    response_model=list[SkillResponse]
)
def get_all_skills(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100
    ),

    sort_by: str = Query(
        default="name",
        pattern="^(name|category|created_at)$"
    ),

    sort_order: str = Query(
        default="asc",
        pattern="^(asc|desc)$"
    ),

    limit: int = Query(
        default=100,
        ge=1,
        le=500
    ),

    db: Session = Depends(get_db)
):

    return skill_service.get_all_skills(
        db=db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit
    )


@router.get(
    "/{skill_id}",
    response_model=SkillResponse
)
def get_skill_by_id(
    skill_id: UUID,
    db: Session = Depends(get_db)
):
    return skill_service.get_skill_by_id(
        db=db,
        skill_id=skill_id
    )


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
    return skill_service.update_skill(
        db=db,
        skill_id=skill_id,
        skill_data=skill_data,
        current_user=current_user
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
    skill_service.delete_skill(
        db=db,
        skill_id=skill_id,
        current_user=current_user
    )
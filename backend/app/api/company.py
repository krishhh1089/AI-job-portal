from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Query, Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User
from app.schemas.company import (
    CreateCompanyRequest,
    UpdateCompanyRequest,
    CompanyResponse,
    CompanyListResponse
)
from app.services.company_service import CompanyService


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post(
    "/",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_company(
    company_data: CreateCompanyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
        return CompanyService.create_company(
            db,
            company_data,
            current_user
        )


@router.get(
    "",
    response_model=CompanyListResponse
)
def get_all_companies(
    search: str | None = Query(default=None),
    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|name|location)$"
    ),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    cursor: str | None = Query(default=None),
    db: Session = Depends(get_db)
):

    return CompanyService.get_all_companies(
        db=db,
        limit=limit,
        cursor=cursor,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get(
    "/{company_id}",
    response_model=CompanyResponse
)
def get_company_by_id(
    company_id: UUID,
    db: Session = Depends(get_db)
):
    company = CompanyService.get_company_by_id(
        db,
        company_id
    )

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found."
        )

    return company


@router.patch(
    "/{company_id}",
    response_model=CompanyResponse
)
def update_company(
    company_id: UUID,
    company_data: UpdateCompanyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = CompanyService.get_company_by_id(
        db,
        company_id
    )

    return CompanyService.update_company(
        db,
        company,
        company_data,
        current_user
    )


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_company(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = CompanyService.get_company_by_id(
        db,
        company_id
    )

    CompanyService.delete_company(
        db,
        company
    )
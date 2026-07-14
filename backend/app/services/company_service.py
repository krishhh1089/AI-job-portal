# app/services/company_service.py

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User, UserRole

from app.repositories.company_repository import company_repository
from app.repositories.user_repository import user_repository

from app.schemas.company import (
    CreateCompanyRequest,
    UpdateCompanyRequest
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    ConflictException
)


class CompanyService:

    # =====================================
    # CREATE
    # =====================================

    @staticmethod
    def create_company(
        db: Session,
        company_data: CreateCompanyRequest,
        recruiter: User
    ) -> Company:

        if recruiter.role != UserRole.RECRUITER:
            raise ForbiddenException(
                "Only recruiters can create companies."
            )

        if recruiter.company_id is not None:
            raise ConflictException(
                "Recruiter already belongs to a company."
            )

        existing_company = company_repository.get_by_name(
            db=db,
            name=company_data.name
        )

        if existing_company:
            raise ConflictException(
                "Company already exists."
            )

        company_dict = company_data.model_dump()

        if company_dict.get("website") is not None:
            company_dict["website"] = str(company_dict["website"])

        if company_dict.get("logo_url") is not None:
            company_dict["logo_url"] = str(company_dict["logo_url"])

        company = Company(**company_dict)

        company = company_repository.create(
            db=db,
            company=company
        )

        recruiter.company_id = company.company_id

        user_repository.update(
            db=db,
            user=recruiter
        )

        return company

    # =====================================
    # READ
    # =====================================

    @staticmethod
    def get_company_by_id(
        db: Session,
        company_id: UUID
    ) -> Company:

        company = company_repository.get_by_id(
            db=db,
            company_id=company_id
        )

        if company is None:
            raise NotFoundException("Company not found.")

        return company

    @staticmethod
    def get_all_companies(
        db: Session,
        limit: int = 20,
        cursor: str | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> dict:

        return company_repository.get_all(
            db=db,
            limit=limit,
            cursor=cursor,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )


    # =====================================
    # UPDATE
    # =====================================

    @staticmethod
    def update_company(
        db: Session,
        company_id: UUID,
        company_data: UpdateCompanyRequest,
        current_user: User
    ) -> Company:

        company = company_repository.get_by_id(
            db=db,
            company_id=company_id
        )

        if company is None:
            raise NotFoundException("Company not found.")

        if current_user.role != UserRole.RECRUITER:
            raise ForbiddenException(
                "Only recruiters can update companies."
            )

        if current_user.company_id != company.company_id:
            raise ForbiddenException(
                "You can update only your own company."
            )

        update_data = company_data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise BadRequestException(
                "No data provided for update."
            )

        if "website" in update_data and update_data["website"] is not None:
            update_data["website"] = str(update_data["website"])

        if "logo_url" in update_data and update_data["logo_url"] is not None:
            update_data["logo_url"] = str(update_data["logo_url"])

        for field, value in update_data.items():
            setattr(company, field, value)

        return company_repository.update(
            db=db,
            company=company
        )

    # =====================================
    # DELETE / DEACTIVATE
    # =====================================

    @staticmethod
    def delete_company(
        db: Session,
        company_id: UUID,
        current_user: User
    ) -> Company:

        company = company_repository.get_by_id(
            db=db,
            company_id=company_id
        )

        if company is None:
            raise NotFoundException("Company not found.")

        if current_user.role != UserRole.RECRUITER:
            raise ForbiddenException(
                "Only recruiters can delete companies."
            )

        if current_user.company_id != company.company_id:
            raise ForbiddenException(
                "You can delete only your own company."
            )

        return company_repository.deactivate(
            db=db,
            company=company
        )


company_service = CompanyService()
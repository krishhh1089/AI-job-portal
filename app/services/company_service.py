from uuid import UUID

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User, UserRole

from app.repositories.company_repository import (
    company_repository
)

from app.repositories.user_repository import (
    user_repository
)

from app.schemas.company import (
    CreateCompanyRequest,
    UpdateCompanyRequest
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

        # ---------------------------------
        # Only recruiters can create company
        # ---------------------------------

        if recruiter.role != UserRole.RECRUITER:
            raise ValueError(
                "Only recruiters can create companies."
            )

        # ---------------------------------
        # Recruiter already has company
        # ---------------------------------

        if recruiter.company_id is not None:
            raise ValueError(
                "Recruiter already belongs to a company."
            )

        # ---------------------------------
        # Company name already exists
        # ---------------------------------

        existing_company = company_repository.get_by_name(
            db,
            company_data.name
        )

        if existing_company:
            raise ValueError(
                "Company already exists."
            )

        # ---------------------------------
        # Create company object
        # ---------------------------------

        company = Company(
            **company_data.model_dump()
        )

        company = company_repository.create(
            db,
            company
        )

        # ---------------------------------
        # Link recruiter with company
        # ---------------------------------

        recruiter.company_id = company.company_id

        user_repository.update(
            db,
            recruiter
        )

        return company
    # =====================================
    # READ
    # =====================================

    @staticmethod
    def get_company_by_id(
        db: Session,
        company_id: UUID
    ) -> Company | None:

        return company_repository.get_by_id(
            db,
            company_id
        )

    @staticmethod
    def get_all_companies(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Company]:

        return company_repository.get_all(
            db,
            skip,
            limit
        )

    # =====================================
    # UPDATE
    # =====================================

    @staticmethod
    def update_company(
        db: Session,
        company: Company,
        company_data: UpdateCompanyRequest
    ) -> Company:

        update_data = company_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                company,
                field,
                value
            )

        return company_repository.update(
            db,
            company
        )

    # =====================================
    # DELETE
    # =====================================

    @staticmethod
    def delete_company(
        db: Session,
        company: Company
    ) -> None:

        company_repository.delete(
            db,
            company
        )
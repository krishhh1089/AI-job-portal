from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:

    # =====================================
    # CREATE
    # =====================================

    def create(
        self,
        db: Session,
        company: Company
    ) -> Company:

        try:
            db.add(company)
            db.commit()
            db.refresh(company)

            return company

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # READ
    # =====================================

    def get_by_id(
        self,
        db: Session,
        company_id: UUID
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(
                Company.company_id == company_id,
                Company.is_active == True
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        name: str
    ) -> Company | None:

        return (
            db.query(Company)
            .filter(
                Company.name == name,
                Company.is_active == True
            )
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[Company]:

        return (
                db.query(Company)
                .filter(Company.is_active == True)
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
        company: Company
    ) -> Company:

        try:
            db.commit()
            db.refresh(company)

            return company

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # DELETE
    # =====================================

    def delete(
        self,
        db: Session,
        company: Company
    ) -> None:

        try:
            db.delete(company)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise

    @staticmethod
    def deactivate(
        db: Session,
        company: Company
    ) -> Company:

        company.is_active = False

        db.commit()
        db.refresh(company)

        return company


# Singleton Instance

company_repository = CompanyRepository()
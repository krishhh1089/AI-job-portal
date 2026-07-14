from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.company import Company
from app.utils.cursor import encode_cursor, decode_cursor
from datetime import datetime

from sqlalchemy import and_, asc, desc, or_
from app.exceptions.custom_exceptions import BadRequestException


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
    limit: int = 20,
    cursor: str | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> dict:

        # Start building the query.
        # Only active companies should be shown.
        query = (
            db.query(Company)
            .filter(Company.is_active == True)
        )

        # =====================================
        # SEARCH
        # =====================================

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Company.name.ilike(search_value),
                    Company.description.ilike(search_value),
                    Company.location.ilike(search_value)
                )
            )

        # =====================================
        # ALLOWED SORTING FIELDS
        # =====================================

        allowed_sort_fields = {
            "created_at": Company.created_at,
            "name": Company.name,
            "location": Company.location
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Company.created_at
        )

        # =====================================
        # CURSOR PAGINATION
        # =====================================

        if cursor:
            cursor_data = decode_cursor(cursor)

            cursor_sort_value = cursor_data["sort_value"]
            cursor_company_id = cursor_data["record_id"]

            # The cursor must be used with the same sorting options
            # that were used when it was created.
            if cursor_data["sort_by"] != sort_by:
                raise BadRequestException(
                    "Cursor does not match sort_by"
                )

            if cursor_data["sort_order"] != sort_order:
                raise BadRequestException(
                    "Cursor does not match sort_order"
                )

            # created_at was stored in the cursor as a string.
            # Convert it back into datetime for database comparison.
            if sort_by == "created_at":
                try:
                    cursor_sort_value = datetime.fromisoformat(
                        cursor_sort_value
                    )
                except ValueError as exc:
                    raise BadRequestException(
                        "Invalid cursor sort value"
                    ) from exc

            # Descending order:
            # values smaller than the last record come next.
            if sort_order == "desc":
                query = query.filter(
                    or_(
                        sort_column < cursor_sort_value,
                        and_(
                            sort_column == cursor_sort_value,
                            Company.company_id < cursor_company_id
                        )
                    )
                )

            # Ascending order:
            # values greater than the last record come next.
            else:
                query = query.filter(
                    or_(
                        sort_column > cursor_sort_value,
                        and_(
                            sort_column == cursor_sort_value,
                            Company.company_id > cursor_company_id
                        )
                    )
                )

        # =====================================
        # APPLY SORTING
        # =====================================

        if sort_order == "asc":
            query = query.order_by(
                asc(sort_column),
                asc(Company.company_id)
            )

        else:
            query = query.order_by(
                desc(sort_column),
                desc(Company.company_id)
            )

        # Fetch one extra company.
        # That extra row tells us whether another page exists.
        companies = query.limit(limit + 1).all()

        has_next = len(companies) > limit

        # Do not return the extra company.
        companies = companies[:limit]

        next_cursor = None

        # =====================================
        # CREATE NEXT CURSOR
        # =====================================

        if has_next and companies:
            last_company = companies[-1]

            if sort_by == "name":
                last_sort_value = last_company.name

            elif sort_by == "location":
                last_sort_value = last_company.location

            else:
                last_sort_value = last_company.created_at

            next_cursor = encode_cursor(
                sort_value=last_sort_value,
                record_id=last_company.company_id,
                sort_by=sort_by,
                sort_order=sort_order
            )

        return {
            "items": companies,
            "next_cursor": next_cursor,
            "has_next": has_next
        }

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
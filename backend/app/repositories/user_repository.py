# app/repositories/user_repository.py

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BadRequestException
from app.models.user import User, UserRole
from app.utils.cursor import decode_cursor, encode_cursor


class UserRepository:

    # =====================================
    # CREATE
    # =====================================

    def create(
        self,
        db: Session,
        user: User
    ) -> User:
        try:
            db.add(user)
            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # READ
    # =====================================

    def get_by_id(
        self,
        db: Session,
        user_id: UUID
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_all(
    self,
    db: Session,
    limit: int = 20,
    cursor: str | None = None,
    search: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
    is_verified: bool | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> dict:

        query = db.query(User)

        # =====================================
        # SEARCH
        # =====================================

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            query = query.filter(
                User.email.ilike(search_value)
            )

        # =====================================
        # FILTERS
        # =====================================

        if role is not None:
            query = query.filter(
                User.role == role
            )

        if is_active is not None:
            query = query.filter(
                User.is_active == is_active
            )

        if is_verified is not None:
            query = query.filter(
                User.is_verified == is_verified
            )

        # =====================================
        # ALLOWED SORTING FIELDS
        # =====================================

        allowed_sort_fields = {
            "created_at": User.created_at,
            "email": User.email,
            "last_login": User.last_login
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            User.created_at
        )

        # =====================================
        # CURSOR PAGINATION
        # =====================================

        if cursor:
            cursor_data = decode_cursor(cursor)

            cursor_sort_value = cursor_data["sort_value"]
            cursor_user_id = cursor_data["record_id"]

            if cursor_data["sort_by"] != sort_by:
                raise BadRequestException(
                    "Cursor does not match sort_by."
                )

            if cursor_data["sort_order"] != sort_order:
                raise BadRequestException(
                    "Cursor does not match sort_order."
                )

            # ---------------------------------
            # last_login can be NULL
            # ---------------------------------

            if sort_by == "last_login":

                # Cursor is already inside the NULL section.
                if cursor_sort_value is None:

                    if sort_order == "desc":
                        query = query.filter(
                            User.last_login.is_(None),
                            User.user_id < cursor_user_id
                        )

                    else:
                        query = query.filter(
                            User.last_login.is_(None),
                            User.user_id > cursor_user_id
                        )

                # Cursor contains an actual last_login datetime.
                else:
                    try:
                        cursor_sort_value = datetime.fromisoformat(
                            cursor_sort_value
                        )

                    except (TypeError, ValueError) as exc:
                        raise BadRequestException(
                            "Invalid user cursor."
                        ) from exc

                    if sort_order == "desc":
                        query = query.filter(
                            or_(
                                User.last_login
                                < cursor_sort_value,

                                and_(
                                    User.last_login
                                    == cursor_sort_value,

                                    User.user_id
                                    < cursor_user_id
                                ),

                                # NULL users come after all
                                # users who have logged in.
                                User.last_login.is_(None)
                            )
                        )

                    else:
                        query = query.filter(
                            or_(
                                User.last_login
                                > cursor_sort_value,

                                and_(
                                    User.last_login
                                    == cursor_sort_value,

                                    User.user_id
                                    > cursor_user_id
                                ),

                                User.last_login.is_(None)
                            )
                        )

            # ---------------------------------
            # Other sorting fields are non-null
            # ---------------------------------

            else:
                if sort_by == "created_at":
                    try:
                        cursor_sort_value = datetime.fromisoformat(
                            cursor_sort_value
                        )

                    except (TypeError, ValueError) as exc:
                        raise BadRequestException(
                            "Invalid user cursor."
                        ) from exc

                if sort_order == "desc":
                    query = query.filter(
                        or_(
                            sort_column < cursor_sort_value,

                            and_(
                                sort_column == cursor_sort_value,
                                User.user_id < cursor_user_id
                            )
                        )
                    )

                else:
                    query = query.filter(
                        or_(
                            sort_column > cursor_sort_value,

                            and_(
                                sort_column == cursor_sort_value,
                                User.user_id > cursor_user_id
                            )
                        )
                    )

        # =====================================
        # APPLY SORTING
        # =====================================

        if sort_by == "last_login":

            if sort_order == "asc":
                query = query.order_by(
                    asc(User.last_login).nulls_last(),
                    asc(User.user_id)
                )

            else:
                query = query.order_by(
                    desc(User.last_login).nulls_last(),
                    desc(User.user_id)
                )

        else:

            if sort_order == "asc":
                query = query.order_by(
                    asc(sort_column),
                    asc(User.user_id)
                )

            else:
                query = query.order_by(
                    desc(sort_column),
                    desc(User.user_id)
                )

        # Fetch one extra user to detect another page.
        users = query.limit(limit + 1).all()

        has_next = len(users) > limit

        # Remove the extra user.
        users = users[:limit]

        next_cursor = None

        # =====================================
        # CREATE NEXT CURSOR
        # =====================================

        if has_next and users:
            last_user = users[-1]

            if sort_by == "email":
                last_sort_value = last_user.email

            elif sort_by == "last_login":
                # This may intentionally be None.
                last_sort_value = last_user.last_login

            else:
                last_sort_value = last_user.created_at

            next_cursor = encode_cursor(
                sort_value=last_sort_value,
                record_id=last_user.user_id,
                sort_by=sort_by,
                sort_order=sort_order
            )

        return {
            "items": users,
            "next_cursor": next_cursor,
            "has_next": has_next
        }

    # =====================================
    # UPDATE
    # =====================================

    def update(
        self,
        db: Session,
        user: User
    ) -> User:
        try:
            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # DELETE
    # =====================================

    def delete(
        self,
        db: Session,
        user: User
    ) -> None:
        try:
            db.delete(user)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # ACCOUNT STATUS
    # =====================================

    def verify_user(
        self,
        db: Session,
        user: User
    ) -> User:
        try:
            user.is_verified = True
            user.email_verification_token = None

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise

    def activate_user(
        self,
        db: Session,
        user: User
    ) -> User:
        try:
            user.is_active = True

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise

    def deactivate_user(
        self,
        db: Session,
        user: User
    ) -> User:
        try:
            user.is_active = False

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise

    # =====================================
    # LOGIN TRACKING
    # =====================================

    def update_last_login(
        self,
        db: Session,
        user: User
    ) -> User:
        try:
            user.last_login = datetime.now(timezone.utc)

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise


# Singleton Instance

user_repository = UserRepository()
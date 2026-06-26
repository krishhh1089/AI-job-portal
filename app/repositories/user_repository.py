# app/repositories/user_repository.py

from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User


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
        skip: int = 0,
        limit: int = 100
    ) -> list[User]:

        return (
            db.query(User)
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
            user.last_login = datetime.now(UTC)

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:
            db.rollback()
            raise


# Singleton Instance

user_repository = UserRepository()
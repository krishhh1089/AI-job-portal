# app/services/user_service.py

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.user_repository import user_repository
from app.schemas.user import UpdateUserRequest


class UserService:

    # =====================================
    # GET USER BY ID
    # =====================================

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: UUID
    ) -> User | None:

        return user_repository.get_by_id(
            db,
            user_id
        )

    # =====================================
    # GET USER BY EMAIL
    # =====================================

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ) -> User | None:

        normalized_email = email.lower().strip()

        return user_repository.get_by_email(
            db,
            normalized_email
        )

    # =====================================
    # GET ALL USERS
    # =====================================

    @staticmethod
    def get_all_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> list[User]:

        return user_repository.get_all(
            db,
            skip,
            limit
        )

    # =====================================
    # UPDATE USER
    # =====================================

    @staticmethod
    def update_user(
        db: Session,
        user: User,
        user_data: UpdateUserRequest
    ) -> User:

        update_data = user_data.model_dump(
            exclude_unset=True
        )

        # -------------------------------
        # Normalize email if updated
        # -------------------------------

        if "email" in update_data:
            new_email = update_data["email"].lower().strip()

            existing_user = user_repository.get_by_email(
                db,
                new_email
            )

            if (
                existing_user
                and existing_user.user_id != user.user_id
            ):
                raise ValueError("Email already exists.")

            update_data["email"] = new_email

        # -------------------------------
        # Prevent dangerous fields update
        # -------------------------------

        blocked_fields = {
            "user_id",
            "password_hash",
            "role",
            "is_verified",
            "is_active",
            "email_verification_token",
            "password_reset_token",
            "password_reset_expires",
            "company_id",
            "created_at",
            "updated_at",
            "last_login",
        }

        for field in blocked_fields:
            update_data.pop(field, None)

        # -------------------------------
        # Apply update
        # -------------------------------

        for field, value in update_data.items():
            setattr(
                user,
                field,
                value
            )

        return user_repository.update(
            db,
            user
        )

    # =====================================
    # VERIFY USER
    # =====================================

    @staticmethod
    def verify_user(
        db: Session,
        user: User
    ) -> User:

        return user_repository.verify_user(
            db,
            user
        )

    # =====================================
    # ACTIVATE USER
    # =====================================

    @staticmethod
    def activate_user(
        db: Session,
        user: User
    ) -> User:

        return user_repository.activate_user(
            db,
            user
        )

    # =====================================
    # DEACTIVATE USER
    # =====================================

    @staticmethod
    def deactivate_user(
        db: Session,
        user: User
    ) -> User:

        return user_repository.deactivate_user(
            db,
            user
        )

    # =====================================
    # UPDATE LAST LOGIN
    # =====================================

    @staticmethod
    def update_last_login(
        db: Session,
        user: User
    ) -> User:

        return user_repository.update_last_login(
            db,
            user
        )

    # =====================================
    # DELETE USER
    # =====================================

    @staticmethod
    def delete_user(
        db: Session,
        user: User
    ) -> None:

        if user.role == UserRole.ADMIN:
            raise ValueError(
                "Admins cannot delete or deactivate their own account."
            )
        
        if user.role == UserRole.JOBSEEKER:
            if user.applications:
                user_repository.deactivate_user(db, user)
                return

            user_repository.delete(db, user)
            return

        if user.role == UserRole.RECRUITER:
            if user.jobs:
                user_repository.deactivate_user(db, user)
                return

            user_repository.delete(db, user)
            return
# app/services/user_service.py

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.user_repository import user_repository
from app.schemas.user import UpdateUserRequest

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    ConflictException
)


class UserService:

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: UUID,
        current_user: User
    ) -> User:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException("Only admins can view users.")

        user = user_repository.get_by_id(
            db=db,
            user_id=user_id
        )

        if user is None:
            raise NotFoundException("User not found.")

        return user

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ) -> User | None:

        normalized_email = email.lower().strip()

        return user_repository.get_by_email(
            db=db,
            email=normalized_email
        )

    @staticmethod
    def get_all_users(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> list[User]:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException("Only admins can view all users.")

        return user_repository.get_all(
            db=db,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def update_user(
        db: Session,
        user: User,
        user_data: UpdateUserRequest
    ) -> User:

        update_data = user_data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise BadRequestException("No data provided for update.")

        if "email" in update_data:
            new_email = update_data["email"].lower().strip()

            existing_user = user_repository.get_by_email(
                db=db,
                email=new_email
            )

            if existing_user and existing_user.user_id != user.user_id:
                raise ConflictException("Email already exists.")

            update_data["email"] = new_email

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

        for field, value in update_data.items():
            setattr(user, field, value)

        return user_repository.update(
            db=db,
            user=user
        )

    @staticmethod
    def verify_user(
        db: Session,
        user: User
    ) -> User:

        return user_repository.verify_user(
            db=db,
            user=user
        )

    @staticmethod
    def activate_user(
        db: Session,
        user_id: UUID,
        current_user: User
    ) -> User:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException("Only admins can activate users.")

        user = user_repository.get_by_id(
            db=db,
            user_id=user_id
        )

        if user is None:
            raise NotFoundException("User not found.")

        return user_repository.activate_user(
            db=db,
            user=user
        )

    @staticmethod
    def deactivate_user(
        db: Session,
        user_id: UUID,
        current_user: User
    ) -> User:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException("Only admins can deactivate users.")

        user = user_repository.get_by_id(
            db=db,
            user_id=user_id
        )

        if user is None:
            raise NotFoundException("User not found.")

        if current_user.user_id == user.user_id:
            raise BadRequestException(
                "Admins cannot deactivate their own account."
            )

        return user_repository.deactivate_user(
            db=db,
            user=user
        )

    @staticmethod
    def update_last_login(
        db: Session,
        user: User
    ) -> User:

        return user_repository.update_last_login(
            db=db,
            user=user
        )

    @staticmethod
    def delete_user(
        db: Session,
        user: User
    ) -> None:

        if user.role == UserRole.ADMIN:
            raise BadRequestException(
                "Admins cannot delete or deactivate their own account."
            )

        if user.role == UserRole.JOBSEEKER:
            if user.applications:
                user_repository.deactivate_user(db=db, user=user)
                return

            user_repository.delete(db=db, user=user)
            return

        if user.role == UserRole.RECRUITER:
            if user.jobs:
                user_repository.deactivate_user(db=db, user=user)
                return

            user_repository.delete(db=db, user=user)
            return


user_service = UserService()
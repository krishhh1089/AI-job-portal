from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.exceptions.custom_exceptions import (
    ConflictException,
    UnauthorizedException,
    ForbiddenException
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user_data: RegisterRequest
    ) -> User:

        email = user_data.email.lower().strip()

        existing_user = user_repository.get_by_email(
            db,
            email
        )

        if existing_user:
            raise ConflictException(
                "Email already registered."
            )

        new_user = User(
            email=email,
            password_hash=hash_password(user_data.password),
            role=user_data.role
        )

        return user_repository.create(
            db,
            new_user
        )

    @staticmethod
    def login(
        db: Session,
        login_data: LoginRequest
    ) -> str:

        email = login_data.email.lower().strip()

        user = user_repository.get_by_email(
            db,
            email
        )

        if user is None:
            raise UnauthorizedException(
                "Invalid email or password."
            )

        if not verify_password(
            login_data.password,
            user.password_hash
        ):
            raise UnauthorizedException(
                "Invalid email or password."
            )

        if not user.is_active:
            raise ForbiddenException(
                "Account is deactivated."
            )

        user_repository.update_last_login(
            db,
            user
        )

        access_token = create_access_token(
            user.user_id
        )

        return access_token
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ) -> User | None:

        return UserRepository.get_by_email(
            db,
            email
        )
    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: UUID
    ) -> User | None:

        return UserRepository.get_by_id(
            db,
            user_id
        )
    
    @staticmethod
    def create_user(
        db: Session,
        user_data: UserCreate
    ) -> User:

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise ValueError(
                "Email already registered."
            )

        new_user = User(

            first_name=user_data.first_name,

            last_name=user_data.last_name,

            email=user_data.email,

            password_hash=user_data.password
        )

        return UserRepository.create(
            db,
            new_user
        )
    @staticmethod
    def update_user(
        db: Session,
        user: User
    ) -> User:

        return UserRepository.update(
            db,
            user
        )
    
    @staticmethod
    def delete_user(
        db: Session,
        user: User
    ):

        UserRepository.delete(
            db,
            user
        )
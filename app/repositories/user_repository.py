from sqlalchemy.orm import Session

from app.models.user import User

from uuid import UUID


class UserRepository:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: UUID
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )
    
    @staticmethod
    def update(
        db: Session,
        user: User
    ) -> User:

        db.commit()
        db.refresh(user)

        return user
    
    @staticmethod
    def delete(
        db: Session,
        user: User
    ):

        db.delete(user)
        db.commit()
    
    @staticmethod
    def create(
        db: Session,
        user: User
    ) -> User:

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
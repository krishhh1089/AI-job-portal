from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def get_user_by_email(
        db,
        email: str
    ):
        return UserRepository.get_by_email(
            db,
            email
        )
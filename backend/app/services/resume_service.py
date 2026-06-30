from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User, UserRole

from app.repositories.resume_repository import resume_repository

from app.schemas.resume import UpdateResumeRequest

from app.utils.file_storage import save_resume
from app.utils.file_validator import validate_resume


class ResumeService:

    @staticmethod
    def upload_resume(
        db: Session,
        file: UploadFile,
        is_default: bool,
        current_user: User
    ) -> Resume:

        if current_user.role != UserRole.JOBSEEKER:
            raise ValueError(
                "Only jobseekers can upload resumes."
            )

        validate_resume(file)

        file_path, file_name = save_resume(file)

        if is_default:
            resume_repository.unset_default_for_user(
                db=db,
                user_id=current_user.user_id
            )

        resume = Resume(
            user_id=current_user.user_id,
            file_name=file_name,
            file_path=file_path,
            is_default=is_default
        )

        return resume_repository.create(
            db=db,
            resume=resume
        )

    @staticmethod
    def get_my_resumes(
        db: Session,
        current_user: User
    ) -> list[Resume]:

        return resume_repository.get_by_user(
            db=db,
            user_id=current_user.user_id
        )

    @staticmethod
    def get_resume_by_id(
        db: Session,
        resume_id: UUID,
        current_user: User
    ) -> Resume:

        resume = resume_repository.get_resume_by_id(
            db=db,
            resume_id=resume_id
        )

        if not resume:
            raise ValueError(
                "Resume not found."
            )

        if resume.user_id != current_user.user_id:
            raise ValueError(
                "You are not allowed to access this resume."
            )

        return resume

    @staticmethod
    def update_resume(
        db: Session,
        resume_id: UUID,
        resume_data: UpdateResumeRequest,
        current_user: User
    ) -> Resume:

        resume = ResumeService.get_resume_by_id(
            db=db,
            resume_id=resume_id,
            current_user=current_user
        )

        update_data = resume_data.model_dump(
            exclude_unset=True
        )

        if "is_default" in update_data:
            if update_data["is_default"] is True:
                resume_repository.unset_default_for_user(
                    db=db,
                    user_id=current_user.user_id
                )

            resume.is_default = update_data.pop("is_default")

        for field, value in update_data.items():
            setattr(resume, field, value)

        return resume_repository.update(
            db=db,
            resume=resume
        )

    @staticmethod
    def delete_resume(
        db: Session,
        resume_id: UUID,
        current_user: User
    ) -> None:

        resume = ResumeService.get_resume_by_id(
            db=db,
            resume_id=resume_id,
            current_user=current_user
        )

        resume_repository.delete(
            db=db,
            resume=resume
        )
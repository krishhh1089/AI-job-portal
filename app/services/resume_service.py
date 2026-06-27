from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User, UserRole

from app.repositories.resume_repository import (
    resume_repository
)

from app.utils.file_storage import (
    save_resume
)

from app.utils.file_validator import validate_resume


class ResumeService:


    @staticmethod
    def upload_resume(
        db: Session,
        file: UploadFile,
        is_default: bool,
        current_user: User
    ) -> Resume:

        # =====================================
        # ONLY JOBSEEKERS
        # =====================================

        if current_user.role != UserRole.JOBSEEKER:
            raise ValueError(
                "Only jobseekers can upload resumes."
            )

        # =====================================
        # VALIDATE FILE
        # =====================================

        validate_resume(file)

        # =====================================
        # SAVE FILE
        # =====================================

        file_path, file_name = save_resume(
            file
        )

        # =====================================
        # HANDLE DEFAULT RESUME
        # =====================================

        if is_default:

            resume_repository.unset_default_for_user(
                db,
                current_user.user_id
            )

        # =====================================
        # CREATE RESUME
        # =====================================

        resume = Resume(

            user_id=current_user.user_id,

            file_path=file_path,

            file_name=file_name,

            is_default=is_default
        )

        return resume_repository.create(
            db,
            resume
        )
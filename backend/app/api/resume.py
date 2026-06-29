from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.dependencies.auth_dependencies import (
    get_current_user
)

from app.models.user import User

from app.schemas.resume import (
    ResumeResponse,
    UpdateResumeRequest
)

from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


# =====================================
# UPLOAD RESUME
# =====================================

@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=201
)
def upload_resume(

    file: UploadFile = File(...),

    is_default: bool = Form(False),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    return ResumeService.upload_resume(

        db=db,

        file=file,

        is_default=is_default,

        current_user=current_user
    )


# =====================================
# GET MY RESUMES
# =====================================

@router.get(
    "/",
    response_model=list[ResumeResponse]
)
def get_my_resumes(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    return ResumeService.get_my_resumes(

        db,

        current_user
    )


# =====================================
# GET ONE RESUME
# =====================================

@router.get(
    "/{resume_id}",
    response_model=ResumeResponse
)
def get_resume(

    resume_id: UUID,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    return ResumeService.get_resume_by_id(

        db,

        resume_id,

        current_user
    )


# =====================================
# UPDATE RESUME
# =====================================

@router.patch(
    "/{resume_id}",
    response_model=ResumeResponse
)
def update_resume(

    resume_id: UUID,

    resume_data: UpdateResumeRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    return ResumeService.update_resume(

        db,

        resume_id,

        resume_data,

        current_user
    )


# =====================================
# DELETE RESUME
# =====================================

@router.delete(
    "/{resume_id}"
)
def delete_resume(

    resume_id: UUID,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    ResumeService.delete_resume(

        db,

        resume_id,

        current_user
    )

    return {
        "message": "Resume deleted successfully."
    }
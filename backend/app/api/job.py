from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.dependencies.auth_dependencies import (
    get_current_user
)

from app.models.user import User

from app.schemas.jobs import (
    CreateJobRequest,
    UpdateJobRequest,
    JobResponse
)

from app.services.job_service import JobService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# =====================================
# CREATE JOB
# =====================================

@router.post(
    "/",
    response_model=JobResponse,
    status_code=201
)
def create_job(
    job_data: CreateJobRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobService.create_job(
        db=db,
        job_data=job_data,
        recruiter=current_user
    )


# =====================================
# GET ALL JOBS
# =====================================

@router.get(
    "/",
    response_model=list[JobResponse]
)
def get_all_jobs(
    db: Session = Depends(get_db)
):
    return JobService.get_all_jobs(db)


# =====================================
# GET JOB BY ID
# =====================================

@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    return JobService.get_job_by_id(
        db,
        job_id
    )


# =====================================
# UPDATE JOB
# =====================================

@router.patch(
    "/{job_id}",
    response_model=JobResponse
)
def update_job(
    job_id: UUID,
    job_data: UpdateJobRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return JobService.update_job(
        db=db,
        job_id=job_id,
        job_data=job_data,
        recruiter=current_user
    )


# =====================================
# DELETE JOB
# =====================================

@router.delete(
    "/{job_id}"
)
def delete_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    JobService.delete_job(
        db=db,
        job_id=job_id,
        recruiter=current_user
    )

    return {
        "message": "Job deleted successfully."
    }
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query
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
    JobResponse,
    JobListResponse
)

from app.services.job_service import JobService
from backend.app.services import job_service


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
    "",
    response_model=JobListResponse
)
def get_all_jobs(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100
    ),

    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|title|salary_min|salary_max)$"
    ),

    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    cursor: str | None = Query(
        default=None
    ),

    db: Session = Depends(get_db)
):
    return job_service.get_all_jobs(
        db=db,
        limit=limit,
        cursor=cursor,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

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
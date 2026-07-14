from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User
from app.models.application import ApplicationStatus

from app.schemas.application import (
    ApplicationResponse,
    ApplicationListResponse,
    UpdateApplicationStatusRequest,
    CreateApplicationRequest
)

from app.services.application_service import ApplicationService


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    application_data: CreateApplicationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

        return ApplicationService.create_application(
            db=db,
            application_data=application_data,
            current_user=current_user
        )


@router.get(
    "/me",
    response_model=ApplicationListResponse
)
def get_my_applications(
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    cursor: str | None = Query(
        default=None
    ),
    status: ApplicationStatus | None = Query(
        default=None
    ),
    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|updated_at)$"
    ),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ApplicationService.get_my_applications(
        db=db,
        current_user=current_user,
        limit=limit,
        cursor=cursor,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = ApplicationService.get_application_by_id(
        db=db,
        application_id=application_id,
        current_user=current_user
    )

    return application


@router.get(
    "/job/{job_id}",
    response_model=ApplicationListResponse
)
def get_job_applications(
    job_id: UUID,
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    cursor: str | None = Query(
        default=None
    ),
    status: ApplicationStatus | None = Query(
        default=None
    ),
    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|updated_at)$"
    ),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ApplicationService.get_job_applications(
        db=db,
        job_id=job_id,
        recruiter=current_user,
        limit=limit,
        cursor=cursor,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponse
)
def update_application_status(
    application_id: UUID,
    application_data: UpdateApplicationStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
        return ApplicationService.update_status(
            db=db,
            application_id=application_id,
            application_data=application_data,
            recruiter=current_user
        )


@router.patch(
    "/{application_id}/withdraw",
    response_model=ApplicationResponse
)
def withdraw_application(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
        return ApplicationService.withdraw_application(
            db=db,
            application_id=application_id,
            current_user=current_user
        )
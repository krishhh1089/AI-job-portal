from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User

from app.schemas.application import (
    CreateApplicationRequest,
    UpdateApplicationStatusRequest,
    ApplicationResponse
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
    try:
        return ApplicationService.create_application(
            db=db,
            application_data=application_data,
            current_user=current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[ApplicationResponse]
)
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ApplicationService.get_my_applications(
            db=db,
            current_user=current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
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
        application_id=application_id
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found."
        )

    if application.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can view only your own application."
        )

    return application


@router.get(
    "/job/{job_id}",
    response_model=list[ApplicationResponse]
)
def get_job_applications(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return ApplicationService.get_job_applications(
            db=db,
            job_id=job_id,
            recruiter=current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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
    try:
        return ApplicationService.update_status(
            db=db,
            application_id=application_id,
            application_data=application_data,
            recruiter=current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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
    try:
        return ApplicationService.withdraw_application(
            db=db,
            application_id=application_id,
            current_user=current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from database import get_db
from models import db_models
from models.schemas import JobCreate, JobResponse, JobType

router = APIRouter()

@router.get("/", response_model=list[JobResponse])
def get_all_jobs(
    # --- pagination ---
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),

    # --- filters ---
    job_type: Optional[JobType] = Query(default=None),
    location: Optional[str] = Query(default=None),
    company: Optional[str] = Query(default=None),

    # --- salary range ---
    salary_min: Optional[int] = Query(default=None, ge=0),
    salary_max: Optional[int] = Query(default=None, ge=0),

    # --- skill filter ---
    skill: Optional[str] = Query(default=None),

    # --- keyword search ---
    search: Optional[str] = Query(default=None),

    db: Session = Depends(get_db)
):
    query = db.query(db_models.Job)

    # filter by job type (exact match)
    if job_type:
        query = query.filter(db_models.Job.job_type == job_type)

    # filter by location (partial, case-insensitive)
    if location:
        query = query.filter(db_models.Job.location.ilike(f"%{location}%"))

    # filter by company (partial, case-insensitive)
    if company:
        query = query.filter(db_models.Job.company.ilike(f"%{company}%"))

    # filter by salary range
    if salary_min is not None:
        query = query.filter(db_models.Job.salary_max >= salary_min)

    if salary_max is not None:
        query = query.filter(db_models.Job.salary_min <= salary_max)

    # filter by skill — checks if skill exists in the array column
    if skill:
        query = query.filter(
            db_models.Job.required_skills.any(skill)
        )

    # keyword search across title AND description
    if search:
        query = query.filter(
            or_(
                db_models.Job.title.ilike(f"%{search}%"),
                db_models.Job.description.ilike(f"%{search}%")
            )
        )

    # sort newest first, then paginate
    jobs = query.order_by(db_models.Job.created_at.desc()).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(db_models.Job).filter(db_models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = db_models.Job(**job.model_dump(), posted_by="recruiter@test.com")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(db_models.Job).filter(db_models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": f"Job {job_id} deleted"}


@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, updated: JobCreate, db: Session = Depends(get_db)):
    job = db.query(db_models.Job).filter(db_models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in updated.model_dump().items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job
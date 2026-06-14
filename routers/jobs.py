from fastapi import APIRouter, HTTPException
from models.schemas import JobCreate, JobResponse

router = APIRouter()

# In-memory store for now (DB comes in Week 2)
jobs_db: list[dict] = []
counter = 1

@router.get("/", response_model=list[JobResponse])
def get_all_jobs(skip: int = 0, limit: int = 10):
    return jobs_db[skip : skip + limit]

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    job = next((j for j in jobs_db if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate):
    global counter
    new_job = {"id": counter, "posted_by": "recruiter@test.com", **job.model_dump()}
    jobs_db.append(new_job)
    counter += 1
    return new_job

@router.delete("/{job_id}")
def delete_job(job_id: int):
    global jobs_db
    job = next((j for j in jobs_db if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    jobs_db = [j for j in jobs_db if j["id"] != job_id]
    return {"message": f"Job {job_id} deleted"}
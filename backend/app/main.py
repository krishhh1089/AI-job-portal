from fastapi import FastAPI

from app.models.base import Base
from app.db.session import engine

from app.models import user, company, skill, jobs, job_skill, resume
from app.api import auth, company, resume, skill, job, application, users


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Job Portal"
)

@app.get("/")
def root():
    return {
        "message": "AI Job Portal API is running"
    }

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(skill.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(application.router)
app.include_router(users.router)
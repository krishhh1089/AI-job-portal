# app/main.py

from fastapi import FastAPI

from app.models.base import Base
from app.db.session import engine



from app.api import (
    auth,
    company,
    resume,
    skill,
    job,
    application,
    users
)

from app.exceptions.handlers import register_exception_handlers



app = FastAPI(
    title="AI Job Portal"
)

register_exception_handlers(app)


@app.get("/")
def root():
    return {
        "message": "AI Job Portal API is running"
    }


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(company.router)
app.include_router(skill.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(application.router)
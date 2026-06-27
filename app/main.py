from fastapi import FastAPI
from app.api import auth, company, resume, skill

from app.api import users
from app.api.users import router as users_router

app = FastAPI(
    title="AI Job Portal",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(skill.router)
app.include_router(job.router)
app.include_router(resume.router)

@app.get("/")
def root():
    return {
        "message": "AI Job Portal API is running"
    }

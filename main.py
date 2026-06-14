from fastapi import FastAPI
from routers import jobs, users

app = FastAPI(
    title="AI Job Portal",
    description="Backend API for AI-powered job portal",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

@app.get("/")
def root():
    return {"message": "AI Job Portal API is running"}
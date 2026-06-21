from fastapi import FastAPI
from database import engine, Base
from models import db_models
from routers import jobs, users

# Create all tables on startup
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Job Portal",
    description="Backend API for AI-powered job portal",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

@app.get("/")
def root():
    return {"message": "AI Job Portal API is running 🚀"}